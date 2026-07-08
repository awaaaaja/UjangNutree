import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import Optional


class ContentBasedFiltering:
    def __init__(self):
        self.food_vectors: Optional[np.ndarray] = None
        self.food_ids: list[str] = []
        self.foods: list[dict] = []
        self.scaler = StandardScaler()
        self._fitted = False

    def fit(self, foods: list[dict]):
        self.foods = foods
        self.food_ids = [f["food_id"] for f in foods]
        features = self._extract_features(foods)
        self.food_vectors = self.scaler.fit_transform(features)
        self._fitted = True

    def _extract_features(self, foods: list[dict]) -> np.ndarray:
        feature_list = []
        for f in foods:
            feature_list.append([
                f.get("energy_kcal", 0) / 100,
                f.get("protein_g", 0) / 10,
                f.get("fat_g", 0) / 10,
                f.get("carbs_g", 0) / 10,
                f.get("fiber_g", 0) / 10,
            ])
        return np.array(feature_list)

    def recommend(self, food_id: str, top_k: int = 10) -> list[dict]:
        if not self._fitted:
            return []

        idx = self.food_ids.index(food_id)
        vector = self.food_vectors[idx].reshape(1, -1)
        similarities = cosine_similarity(vector, self.food_vectors).flatten()

        similar_indices = np.argsort(similarities)[::-1][1:top_k + 1]
        results = []
        for i in similar_indices:
            results.append({
                **self.foods[i],
                "score": float(similarities[i]),
                "reason": f"CBF similarity: {similarities[i]:.3f}"
            })
        return results

    def recommend_by_profile(self, target_nutrition: dict, top_k: int = 10) -> list[dict]:
        if not self._fitted:
            return []

        target_vec = np.array([[
            target_nutrition.get("energy_kcal", 0) / 100,
            target_nutrition.get("protein_g", 0) / 10,
            target_nutrition.get("fat_g", 0) / 10,
            target_nutrition.get("carbs_g", 0) / 10,
            target_nutrition.get("fiber_g", 0) / 10,
        ]])
        target_vec = self.scaler.transform(target_vec)

        similarities = cosine_similarity(target_vec, self.food_vectors).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for i in top_indices:
            results.append({
                **self.foods[i],
                "score": float(similarities[i]),
                "reason": f"CBF profile match: {similarities[i]:.3f}"
            })
        return results