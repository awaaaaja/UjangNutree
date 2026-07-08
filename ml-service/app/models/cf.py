import numpy as np
from typing import Optional


class CollaborativeFiltering:
    def __init__(self, n_factors: int = 20, n_epochs: int = 50, lr: float = 0.01, reg: float = 0.02):
        self.n_factors = n_factors
        self.n_epochs = n_epochs
        self.lr = lr
        self.reg = reg
        self.user_factors: Optional[np.ndarray] = None
        self.item_factors: Optional[np.ndarray] = None
        self.user_map: dict[str, int] = {}
        self.item_map: dict[str, int] = {}
        self.reverse_item_map: dict[int, str] = {}
        self.food_data: dict[str, dict] = {}
        self._fitted = False

    def fit(self, interactions: list[dict]):
        users = list(set(i["patient_id"] for i in interactions))
        items = list(set(i["food_id"] for i in interactions))

        self.user_map = {u: idx for idx, u in enumerate(users)}
        self.item_map = {f: idx for idx, f in enumerate(items)}
        self.reverse_item_map = {idx: f for f, idx in self.item_map.items()}

        for i in interactions:
            self.food_data[i["food_id"]] = {k: v for k, v in i.items() if k not in ("patient_id", "food_id", "rating")}

        n_users = len(users)
        n_items = len(items)

        self.user_factors = np.random.normal(0, 0.1, (n_users, self.n_factors))
        self.item_factors = np.random.normal(0, 0.1, (n_items, self.n_factors))

        ratings_matrix = np.zeros((n_users, n_items))
        for i in interactions:
            u = self.user_map[i["patient_id"]]
            v = self.item_map[i["food_id"]]
            ratings_matrix[u, v] = i.get("rating", 1)

        for epoch in range(self.n_epochs):
            for u in range(n_users):
                for v in range(n_items):
                    if ratings_matrix[u, v] == 0:
                        continue
                    pred = np.dot(self.user_factors[u], self.item_factors[v])
                    err = ratings_matrix[u, v] - pred

                    self.user_factors[u] += self.lr * (err * self.item_factors[v] - self.reg * self.user_factors[u])
                    self.item_factors[v] += self.lr * (err * self.user_factors[u] - self.reg * self.item_factors[v])

        self._fitted = True

    def recommend(self, patient_id: str, top_k: int = 10) -> list[dict]:
        if not self._fitted or patient_id not in self.user_map:
            return []

        u = self.user_map[patient_id]
        scores = self.item_factors @ self.user_factors[u]
        top_items = np.argsort(scores)[::-1][:top_k]

        results = []
        for item_idx in top_items:
            food_id = self.reverse_item_map[item_idx]
            food_info = self.food_data.get(food_id, {})
            results.append({
                "food_id": food_id,
                **food_info,
                "score": float(scores[item_idx]),
                "reason": f"CF collaborative score: {scores[item_idx]:.3f}"
            })
        return results

    def predict_rating(self, patient_id: str, food_id: str) -> float:
        if not self._fitted or patient_id not in self.user_map or food_id not in self.item_map:
            return 0.0
        u = self.user_map[patient_id]
        v = self.item_map[food_id]
        return float(np.dot(self.user_factors[u], self.item_factors[v]))