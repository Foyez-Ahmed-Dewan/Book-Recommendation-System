import numpy as np
import pandas as pd


class EmbeddingRecommender:
    def __init__(self, books_df, embeddings, model):
        self.books = books_df.reset_index(drop=True)
        self.embeddings = embeddings
        self.model = model

    def _safe_str_contains(self, series, value):
        return series.fillna("").astype(str).str.contains(str(value), case=False, na=False)

    def apply_filters(self, df, filters=None):
        if not filters:
            return df

        filtered = df.copy()

        genre = filters.get("genre")
        author = filters.get("author")
        min_rating = filters.get("min_rating")

        if genre:
            filtered = filtered[self._safe_str_contains(filtered["genre"], genre)]

        if author:
            filtered = filtered[self._safe_str_contains(filtered["author"], author)]

        if min_rating is not None:
            filtered = filtered[filtered["rating"] >= min_rating]

        return filtered

    def _format_output(self, df):
        output_cols = [
            col for col in [
                "title",
                "author",
                "genre",
                "rating",
                "totalratings",
                "weighted_score",
                "img"
            ]
            if col in df.columns
        ]
        return df[output_cols]

    def get_popular_books(self, top_k=10, filters=None):
        filtered = self.apply_filters(self.books, filters)

        if filtered.empty:
            return pd.DataFrame()

        popular = filtered.sort_values(
            by="weighted_score",
            ascending=False
        ).head(top_k)

        return self._format_output(popular)

    def recommend(self, query=None, top_k=10, filters=None):
        # Case: filter only
        if not query or not query.strip():
            return self.get_popular_books(top_k=top_k, filters=filters)

        filtered_books = self.apply_filters(self.books, filters)

        if filtered_books.empty:
            return pd.DataFrame()

        formatted_query = f"query: {query.strip()}"

        query_embedding = self.model.encode(
            formatted_query,
            normalize_embeddings=True
        )

        candidate_indices = filtered_books.index.to_numpy()
        candidate_embeddings = self.embeddings[candidate_indices]

        similarities = np.dot(candidate_embeddings, query_embedding)

        top_local_indices = np.argsort(similarities)[::-1][:top_k]
        top_global_indices = candidate_indices[top_local_indices]

        results = self.books.iloc[top_global_indices].copy()

        return self._format_output(results)