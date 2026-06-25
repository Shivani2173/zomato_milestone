"""
main.py
-------
FastAPI entrypoint for the AI-Powered Restaurant Recommendation API.

Endpoints
---------
POST /api/recommend   – Filter dataset + invoke Groq LLM, return ranked recommendations.
GET  /api/locations   – Return unique locations available in the dataset (for UI dropdown).
GET  /api/cuisines    – Return unique cuisines available in the dataset (for UI dropdown).
GET  /                – Health-check / welcome message.

Milestone 4 Verification
------------------------
Run from the *backend/* directory with:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs to explore and test via Swagger UI.
"""

from contextlib import asynccontextmanager
from typing import List

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_db
from app.engine import filter_restaurants
from app.recommender import get_recommendations
from app.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    RestaurantRecommendation,
    LocationsResponse,
    CuisinesResponse,
)

# ---------------------------------------------------------------------------
# Application-level state (dataset loaded once at startup)
# ---------------------------------------------------------------------------

_state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load (and cache) the dataset exactly once when the server starts."""
    print("[startup] Loading Zomato dataset …")
    _state["df"] = get_db()
    print(f"[startup] Dataset ready — {len(_state['df'])} restaurants loaded.")
    yield
    # (cleanup on shutdown if needed)
    _state.clear()


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Zomato AI Restaurant Recommender",
    description=(
        "An AI-powered restaurant recommendation API that combines structured "
        "dataset filtering with Groq LLM-generated explanations."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins so the standalone frontend (file://) and any local
# dev server can call the API without being blocked.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helper: safe DataFrame access
# ---------------------------------------------------------------------------

def _get_df() -> pd.DataFrame:
    df = _state.get("df")
    if df is None or df.empty:
        raise HTTPException(
            status_code=503,
            detail="Dataset is not available. Please try again in a moment.",
        )
    return df


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    """Health-check endpoint."""
    df = _state.get("df")
    total = len(df) if df is not None else 0
    return {
        "status": "ok",
        "message": "Zomato AI Recommender API is running.",
        "restaurants_loaded": total,
    }


@app.get("/api/locations", response_model=LocationsResponse, tags=["Metadata"])
def get_locations():
    """
    Return the sorted list of unique restaurant locations present in the
    dataset. Intended for populating the Location dropdown in the UI.
    """
    df = _get_df()
    locations: List[str] = (
        df["location"]
        .dropna()
        .unique()
        .tolist()
    )
    locations = sorted(set(loc.strip() for loc in locations if loc.strip()))
    return LocationsResponse(locations=locations)


@app.get("/api/cuisines", response_model=CuisinesResponse, tags=["Metadata"])
def get_cuisines():
    """
    Return the sorted list of unique cuisines present in the dataset.
    The cuisines column stores Python lists per row; this endpoint flattens
    and de-duplicates them. Intended for populating the Cuisine dropdown.
    """
    df = _get_df()
    all_cuisines: set = set()
    for cuisine_list in df["cuisines"].dropna():
        if isinstance(cuisine_list, list):
            for c in cuisine_list:
                if c and c.strip():
                    all_cuisines.add(c.strip())
    return CuisinesResponse(cuisines=sorted(all_cuisines))


@app.post("/api/recommend", response_model=RecommendationResponse, tags=["Recommendations"])
def recommend(request: RecommendationRequest):
    """
    Core recommendation endpoint.

    1. Validate and extract user preferences from the request body.
    2. Filter the dataset using the structured engine (location / cuisine /
       budget / min_rating).
    3. If no candidates match the filters, return an empty list with a
       descriptive message rather than raising an error.
    4. Pass the candidate list to the Groq LLM recommender, which ranks and
       explains the top 3 choices.
    5. Return the ranked recommendations wrapped in a standard envelope.
    """
    df = _get_df()

    # --- Step 1: Filter candidates ---
    candidates = filter_restaurants(
        df=df,
        location=request.location or "",
        cuisine=request.cuisine or "",
        budget=request.budget or "",
        min_rating=request.min_rating,
        limit=15,  # over-fetch slightly so the LLM has richer context
    )

    # --- Step 2: Handle zero-match case gracefully ---
    if candidates.empty:
        return RecommendationResponse(
            success=True,
            count=0,
            recommendations=[],
            message=(
                "No restaurants matched your filters. "
                "Try relaxing the location, cuisine, budget, or rating criteria."
            ),
        )

    # --- Step 3: Invoke LLM recommender ---
    raw_recs: list = get_recommendations(
        candidates_df=candidates,
        location=request.location or "",
        cuisine=request.cuisine or "",
        budget=request.budget or "",
        min_rating=request.min_rating,
        notes=request.notes or "",
    )

    # --- Step 4: Validate and coerce each recommendation ---
    validated: List[RestaurantRecommendation] = []
    for rec in raw_recs:
        try:
            validated.append(
                RestaurantRecommendation(
                    name=str(rec.get("name", "Unknown")),
                    cuisine=str(rec.get("cuisine", "")),
                    rating=float(rec.get("rating", 0.0)),
                    estimated_cost=int(rec.get("estimated_cost", 0)),
                    ai_explanation=str(rec.get("ai_explanation", "")),
                )
            )
        except Exception as parse_err:
            # Skip malformed entries rather than crashing the whole response
            print(f"[WARN] Skipping malformed recommendation entry: {parse_err}")

    return RecommendationResponse(
        success=True,
        count=len(validated),
        recommendations=validated,
        message=None if validated else "The AI could not generate recommendations. Please try again.",
    )
