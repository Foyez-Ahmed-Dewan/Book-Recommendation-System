from app.artifact_loader import load_artifacts
from app.model_loader import load_embedding_model
from app.recommender import EmbeddingRecommender


def create_recommender():
    books, embeddings = load_artifacts()
    model = load_embedding_model()

    recommender = EmbeddingRecommender(
        books_df=books,
        embeddings=embeddings,
        model=model
    )

    return recommender  


# global instance
recommender = create_recommender()