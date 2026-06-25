import json
import re
from groq import Groq
import pandas as pd
from app.config import GROQ_API_KEY, GROQ_MODEL

def generate_fallback_recommendations(candidates_df: pd.DataFrame, notes: str = "") -> list:
    """
    Generate mock structured recommendations from candidate restaurants.
    Used as a graceful fallback when GROQ_API_KEY is missing, invalid, or rate-limited.
    """
    recommendations = []
    
    # Take top 3 candidates (they are already sorted by rating and votes descending)
    top_candidates = candidates_df.head(3)
    
    for _, row in top_candidates.iterrows():
        name = row['name']
        cuisines_list = row['cuisines']
        cuisines_str = ", ".join(cuisines_list) if isinstance(cuisines_list, list) else str(cuisines_list)
        rate = float(row['rate'])
        cost = int(row['approx_cost(for two people)'])
        location = row['location']
        dish_liked = row.get('dish_liked', '')
        
        # Build a customized reason using the available data fields
        reason = f"Excellent choice in {location} serving {cuisines_str}."
        if pd.notna(dish_liked) and dish_liked:
            reason += f" Customer favorites include {dish_liked}."
        reason += f" It fits your criteria perfectly with a strong rating of {rate}/5."
        
        if notes and notes.strip():
            reason += f" Matches your custom request for '{notes}' due to its popular menu and great service."
            
        recommendations.append({
            "name": name,
            "cuisine": cuisines_str,
            "rating": rate,
            "estimated_cost": cost,
            "ai_explanation": reason
        })
        
    return recommendations

def get_recommendations(
    candidates_df: pd.DataFrame,
    location: str = "",
    cuisine: str = "",
    budget: str = "",
    min_rating: float = 0.0,
    notes: str = ""
) -> list:
    """
    Formulate prompts, query the Groq LLM API to rank and explain restaurant recommendations,
    and parse the structured JSON response. Falls back gracefully on error/key missing.
    """
    # Boundary check: If no candidates match, return empty immediately
    if candidates_df.empty:
        return []

    # API Validation: Check if API key is missing or set to placeholder
    is_placeholder = GROQ_API_KEY in ("", "your_groq_api_key_here")
    
    if is_placeholder:
        print("[WARNING] GROQ_API_KEY is not configured or is a placeholder. Using local rule-based fallback recommender.")
        return generate_fallback_recommendations(candidates_df, notes)

    # Format candidate data for prompt context
    # Selecting only necessary fields to conserve token usage
    simplified_candidates = []
    for _, row in candidates_df.iterrows():
        simplified_candidates.append({
            "name": row['name'],
            "location": row['location'],
            "cuisines": row['cuisines'],
            "approx_cost_for_two": int(row['approx_cost(for two people)']),
            "rating": float(row['rate']),
            "votes": int(row['votes']),
            "popular_dishes": row.get('dish_liked', '')
        })

    candidates_json = json.dumps(simplified_candidates, indent=2)

    # Construct Prompts
    system_instruction = (
        "You are an expert culinary guide and local restaurant recommender.\n"
        "Your task is to rank the candidate restaurants and write a personalized explanation "
        "describing why each restaurant is a great match for the user's preferences (especially matching "
        "their custom qualitative notes).\n\n"
        "You MUST return a raw JSON array matching this schema structure, without any conversational prefix or suffix:\n"
        "[\n"
        "  {\n"
        "    \"name\": \"Restaurant Name\",\n"
        "    \"cuisine\": \"Cuisine(s) list\",\n"
        "    \"rating\": 4.2,\n"
        "    \"estimated_cost\": 800,\n"
        "    \"ai_explanation\": \"2-3 sentence explanation explaining why it fits budget/taste/notes.\"\n"
        "  }\n"
        "]\n\n"
        "Strict Constraints:\n"
        "1. Recommend ONLY restaurants present in the provided candidates list. Do not hallucinate external names.\n"
        "2. Do not include markdown wraps (e.g. ```json) or explanation texts around the JSON array. Output raw JSON code.\n"
        "3. Provide exactly the top 3 recommendations from the candidate list."
    )

    user_query = (
        f"User Preference Filters:\n"
        f"- Location: {location}\n"
        f"- Cuisine: {cuisine}\n"
        f"- Budget Range: {budget}\n"
        f"- Minimum Rating: {min_rating}\n"
        f"- Additional Preferences / Notes: {notes}\n\n"
        f"Candidate Restaurants List:\n"
        f"{candidates_json}"
    )

    try:
        # Initialize Groq Client
        client = Groq(api_key=GROQ_API_KEY)
        
        # Request completion
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_query}
            ],
            temperature=0.3,
            max_tokens=800
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Clean response string to parse as JSON (handles potential markdown wrap bugs)
        if "```" in response_text:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", response_text)
            if match:
                response_text = match.group(1).strip()
                
        # Parse JSON
        results = json.loads(response_text)
        if isinstance(results, list):
            return results
        else:
            print(f"[ERROR] LLM returned non-list JSON: {response_text}")
            return generate_fallback_recommendations(candidates_df, notes)

    except Exception as e:
        print(f"[ERROR] Groq API call failed: {e}. Falling back to rule-based recommender.")
        return generate_fallback_recommendations(candidates_df, notes)

if __name__ == "__main__":
    print("Testing Groq recommender integration standalone...")
    from app.database import get_db
    from app.engine import filter_restaurants

    df = get_db()
    
    # 1. Test case: Filter candidates
    candidates = filter_restaurants(
        df, 
        location="Banashankari", 
        cuisine="Chinese", 
        budget="medium", 
        min_rating=4.0
    )
    
    print(f"Candidates found: {len(candidates)}")
    
    # Run recommender (will fallback to local mock recommendations if key is missing/unconfigured)
    recommendations = get_recommendations(
        candidates_df=candidates,
        location="Banashankari",
        cuisine="Chinese",
        budget="medium",
        min_rating=4.0,
        notes="spicy food, family friendly dinner"
    )
    
    print("\nFinal Recommendations:")
    print(json.dumps(recommendations, indent=2))
