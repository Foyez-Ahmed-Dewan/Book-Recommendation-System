import json
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.recommender_service import recommender
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.core.security import get_current_user
from app.db.database import get_db
from app.db.models import User, SearchHistory

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/health")
def recommendation_health():
    return {
        "status": "ok",
        "service": "recommendation-route"
    }


@router.post("/", response_model=RecommendationResponse)
def get_recommendations(
    payload: RecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        filters = {
            "genre": payload.genre,
            "author": payload.author,
            "min_rating": payload.min_rating,
        }

        filters = {k: v for k, v in filters.items() if v is not None}

        results_df = recommender.recommend(
            query=payload.query,
            top_k=payload.top_k,
            filters=filters if filters else None
        )

        if results_df is None or results_df.empty:
            history = SearchHistory(
                user_id=current_user.id,
                query=payload.query,
                genre=payload.genre,
                author=payload.author,
                min_rating=payload.min_rating,
                top_k=payload.top_k,
                results_json=json.dumps([])
            )
            db.add(history)
            db.commit()

            return RecommendationResponse(
                message="No books found for the given query/filters.",
                count=0,
                results=[]
            )

        results_df = results_df.where(pd.notnull(results_df), None)
        results = results_df.to_dict(orient="records")

        history = SearchHistory(
            user_id=current_user.id,
            query=payload.query,
            genre=payload.genre,
            author=payload.author,
            min_rating=payload.min_rating,
            top_k=payload.top_k,
            results_json=json.dumps(results)
        )
        db.add(history)
        db.commit()

        return RecommendationResponse(
            message="Recommendations fetched successfully.",
            count=len(results),
            results=results
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(e)}"
        )
        

@router.get("/trending")
def get_trending_books(
    current_user: User = Depends(get_current_user)
):
    results_df = recommender.get_popular_books(top_k=5)

    if results_df is None or results_df.empty:
        return {
            "message": "No trending books found.",
            "count": 0,
            "results": []
        }

    results_df = results_df.where(pd.notnull(results_df), None)
    results = results_df.to_dict(orient="records")

    return {
        "message": "Trending books fetched successfully.",
        "count": len(results),
        "results": results
    }
    
    

@router.get("/recent")
def get_recent_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rows = (
        db.query(SearchHistory)
        .filter(SearchHistory.user_id == current_user.id)
        .order_by(SearchHistory.created_at.desc())
        .all()
    )

    books = []
    seen_titles = set()

    for row in rows:
        row_results = json.loads(row.results_json) if row.results_json else []

        for book in row_results:
            title = book.get("title")
            if title and title not in seen_titles:
                seen_titles.add(title)
                books.append(book)

            if len(books) == 5:
                break

        if len(books) == 5:
            break

    return {
        "message": "Recent recommendations fetched successfully.",
        "count": len(books),
        "results": books
    }