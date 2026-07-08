import pytest
import numpy as np
from app.models.cbf import ContentBasedFiltering
from app.models.cf import CollaborativeFiltering


@pytest.fixture
def sample_foods():
    return [
        {"food_id": "f001", "name": "Nasi Putih", "energy_kcal": 180, "protein_g": 3, "fat_g": 0.3, "carbs_g": 40, "fiber_g": 0.5},
        {"food_id": "f002", "name": "Ayam Goreng", "energy_kcal": 250, "protein_g": 25, "fat_g": 15, "carbs_g": 2, "fiber_g": 0},
        {"food_id": "f003", "name": "Tempe Goreng", "energy_kcal": 200, "protein_g": 20, "fat_g": 10, "carbs_g": 8, "fiber_g": 2},
        {"food_id": "f004", "name": "Sayur Bayam", "energy_kcal": 30, "protein_g": 3, "fat_g": 0.5, "carbs_g": 5, "fiber_g": 2},
        {"food_id": "f005", "name": "Ikan Bakar", "energy_kcal": 150, "protein_g": 30, "fat_g": 3, "carbs_g": 0, "fiber_g": 0},
    ]


@pytest.fixture
def sample_interactions():
    return [
        {"patient_id": "p001", "food_id": "f001", "rating": 5.0},
        {"patient_id": "p001", "food_id": "f002", "rating": 4.0},
        {"patient_id": "p001", "food_id": "f005", "rating": 3.0},
        {"patient_id": "p002", "food_id": "f001", "rating": 2.0},
        {"patient_id": "p002", "food_id": "f003", "rating": 5.0},
        {"patient_id": "p002", "food_id": "f004", "rating": 4.0},
        {"patient_id": "p003", "food_id": "f005", "rating": 5.0},
        {"patient_id": "p003", "food_id": "f002", "rating": 3.0},
        {"patient_id": "p003", "food_id": "f003", "rating": 4.0},
    ]


class TestCBF:
    def test_fit_and_recommend(self, sample_foods):
        cbf = ContentBasedFiltering()
        cbf.fit(sample_foods)
        assert cbf._fitted == True
        assert cbf.food_vectors.shape == (5, 5)

    def test_recommend_returns_different_foods(self, sample_foods):
        cbf = ContentBasedFiltering()
        cbf.fit(sample_foods)
        recs = cbf.recommend("f001", top_k=3)
        assert len(recs) <= 3
        assert all(r["food_id"] != "f001" for r in recs)

    def test_recommend_by_profile(self, sample_foods):
        cbf = ContentBasedFiltering()
        cbf.fit(sample_foods)
        target = {"energy_kcal": 200, "protein_g": 20, "fat_g": 10, "carbs_g": 10, "fiber_g": 2}
        recs = cbf.recommend_by_profile(target, top_k=3)
        assert len(recs) <= 3
        assert all("score" in r for r in recs)

    def test_recommend_without_fit(self):
        cbf = ContentBasedFiltering()
        assert cbf.recommend("f001") == []
        assert cbf.recommend_by_profile({"energy_kcal": 100}) == []


class TestCF:
    def test_fit_and_predict(self, sample_interactions):
        cf = CollaborativeFiltering(n_factors=5, n_epochs=10)
        cf.fit(sample_interactions)
        assert cf._fitted == True
        assert len(cf.user_map) == 3
        assert len(cf.item_map) == 5

    def test_predict_rating(self, sample_interactions):
        cf = CollaborativeFiltering(n_factors=5, n_epochs=10)
        cf.fit(sample_interactions)
        rating = cf.predict_rating("p001", "f001")
        assert isinstance(rating, float)

    def test_predict_unknown_user(self, sample_interactions):
        cf = CollaborativeFiltering(n_factors=5, n_epochs=10)
        cf.fit(sample_interactions)
        rating = cf.predict_rating("unknown", "f001")
        assert rating == 0.0

    def test_recommend_for_user(self, sample_interactions):
        cf = CollaborativeFiltering(n_factors=5, n_epochs=10)
        cf.fit(sample_interactions)
        recs = cf.recommend("p001", top_k=3)
        assert len(recs) <= 3
        assert all("score" in r for r in recs)

    def test_recommend_unknown_user(self, sample_interactions):
        cf = CollaborativeFiltering(n_factors=5, n_epochs=10)
        cf.fit(sample_interactions)
        recs = cf.recommend("unknown")
        assert recs == []