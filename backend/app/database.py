import pandas as pd
import re
import ast
from datasets import load_dataset
from app.config import CACHE_FILE_PATH

def clean_rating(val):
    if pd.isna(val) or not isinstance(val, str):
        return 0.0
    val = val.strip()
    if val in ("NEW", "-", ""):
        return 0.0
    # Extract rating value, e.g. "4.1/5" -> 4.1, "4.1" -> 4.1
    match = re.match(r"^([0-9.]+)", val)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    return 0.0

def clean_cost(val):
    if pd.isna(val):
        return 0
    if isinstance(val, (int, float)):
        return int(val)
    val = str(val).strip()
    # Strip commas and any non-digit character
    cleaned = re.sub(r"[^\d]", "", val)
    if cleaned:
        try:
            return int(cleaned)
        except ValueError:
            return 0
    return 0

def clean_cuisines(val):
    if pd.isna(val) or not isinstance(val, str):
        return []
    # Split by comma and strip spaces
    return [c.strip() for c in val.split(",") if c.strip()]

def get_db():
    """
    Load the dataset. If cached copy exists, load it directly.
    Otherwise download from Hugging Face, clean, cache, and return.
    """
    if CACHE_FILE_PATH.exists():
        print(f"Loading cached dataset from {CACHE_FILE_PATH}...")
        # Note: when reading from CSV, list columns are saved as string representations (e.g. "['Italian', 'Pizza']")
        # We need to parse them back to lists.
        df = pd.read_csv(CACHE_FILE_PATH)
        # Safely evaluate list strings back to python lists
        df['cuisines'] = df['cuisines'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else [])
        return df

    print("Cache not found. Fetching dataset from Hugging Face...")
    try:
        # Load Hugging Face dataset
        dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
        df = pd.DataFrame(dataset)
    except Exception as e:
        print(f"Error downloading from Hugging Face: {e}")
        print("Initializing empty database as fallback.")
        df = pd.DataFrame(columns=[
            'name', 'online_order', 'book_table', 'rate', 'votes', 
            'location', 'rest_type', 'dish_liked', 'cuisines', 
            'approx_cost(for two people)', 'reviews_list', 'menu_item', 
            'listed_in(type)', 'listed_in(city)'
        ])
        return df

    print("Cleaning and preprocessing dataset...")
    # Deduplicate rows
    df.drop_duplicates(subset=['name', 'address', 'location'], inplace=True, keep='first')
    
    # Process fields
    df['rate'] = df['rate'].apply(clean_rating)
    df['approx_cost(for two people)'] = df['approx_cost(for two people)'].apply(clean_cost)
    df['cuisines'] = df['cuisines'].apply(clean_cuisines)
    df['location'] = df['location'].fillna("").apply(lambda x: x.strip())
    df['name'] = df['name'].fillna("").apply(lambda x: x.strip())
    
    # Save cache
    print(f"Saving cached dataset to {CACHE_FILE_PATH}...")
    df.to_csv(CACHE_FILE_PATH, index=False)
    
    return df

if __name__ == "__main__":
    # Test script standalone to build and verify cache
    print("Testing data ingestion standalone...")
    df = get_db()
    print(f"Data ingestion successful. Total unique restaurants: {len(df)}")
    print("Columns in cache:", df.columns.tolist())
    print("\nSample Rows:")
    print(df[['name', 'rate', 'location', 'cuisines', 'approx_cost(for two people)']].head(3))
