import pandas as pd
from app.database import get_db

def filter_restaurants(
    df: pd.DataFrame,
    location: str = None,
    cuisine: str = None,
    budget: str = None,
    min_rating: float = 0.0,
    limit: int = 10
) -> pd.DataFrame:
    """
    Filter the restaurants DataFrame based on location, cuisine, budget, and rating constraints.
    Sort by rating and votes descending, and slice to the requested limit.
    """
    filtered_df = df.copy()
    if filtered_df.empty:
        return filtered_df
    
    # 1. Filter by Location (case-insensitive substring match)
    if location and isinstance(location, str) and location.strip():
        loc_cleaned = location.strip().lower()
        filtered_df = filtered_df[filtered_df['location'].str.lower().str.contains(loc_cleaned, na=False)]
        if filtered_df.empty:
            return filtered_df
        
    # 2. Filter by Cuisine (case-insensitive list search)
    if cuisine and isinstance(cuisine, str) and cuisine.strip():
        cui_cleaned = cuisine.strip().lower()
        # cuisines is represented as a list of cleaned cuisines in each row
        filtered_df = filtered_df[filtered_df['cuisines'].apply(
            lambda cuisines_list: any(cui_cleaned == c.lower() for c in cuisines_list)
        )]
        if filtered_df.empty:
            return filtered_df
        
    # 3. Filter by Rating (rating >= min_rating)
    if min_rating and min_rating > 0.0:
        filtered_df = filtered_df[filtered_df['rate'] >= min_rating]
        if filtered_df.empty:
            return filtered_df
        
    # 4. Filter by Budget Range
    # low: cost < 500
    # medium: 500 <= cost <= 1500
    # high: cost > 1500
    if budget and isinstance(budget, str) and budget.strip():
        budget_cleaned = budget.strip().lower()
        if budget_cleaned == 'low':
            filtered_df = filtered_df[filtered_df['approx_cost(for two people)'] < 500]
        elif budget_cleaned == 'medium':
            filtered_df = filtered_df[(filtered_df['approx_cost(for two people)'] >= 500) & (filtered_df['approx_cost(for two people)'] <= 1500)]
        elif budget_cleaned == 'high':
            filtered_df = filtered_df[filtered_df['approx_cost(for two people)'] > 1500]
        if filtered_df.empty:
            return filtered_df

    # 5. Sort by rating descending, then votes descending
    filtered_df = filtered_df.sort_values(by=['rate', 'votes'], ascending=[False, False])
    
    # 6. Apply limit
    return filtered_df.head(limit)

if __name__ == "__main__":
    print("Testing local search and query engine...")
    df = get_db()
    
    # Test 1: Standard query
    print("\n--- Test 1: Banashankari, Chinese, Medium Budget, Rating >= 4.0 ---")
    results_1 = filter_restaurants(
        df, 
        location="Banashankari", 
        cuisine="Chinese", 
        budget="medium", 
        min_rating=4.0, 
        limit=5
    )
    print(f"Matches found: {len(results_1)}")
    if not results_1.empty:
        print(results_1[['name', 'location', 'cuisines', 'approx_cost(for two people)', 'rate', 'votes']])
        
    # Test 2: Substring Location match ("Banas" should match "Banashankari")
    print("\n--- Test 2: Location substring 'Banas', North Indian, Low Budget ---")
    results_2 = filter_restaurants(
        df, 
        location="Banas", 
        cuisine="North Indian", 
        budget="low", 
        min_rating=3.5, 
        limit=3
    )
    print(f"Matches found: {len(results_2)}")
    if not results_2.empty:
        print(results_2[['name', 'location', 'cuisines', 'approx_cost(for two people)', 'rate', 'votes']])
        
    # Test 3: Zero matches query
    print("\n--- Test 3: Non-existent Location, Italian ---")
    results_3 = filter_restaurants(
        df, 
        location="NonExistentCity123", 
        cuisine="Italian"
    )
    print(f"Matches found: {len(results_3)} (Expected: 0)")
    assert results_3.empty
    print("Zero matches handled gracefully.")
