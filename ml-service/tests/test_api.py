import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.anyio
async def test_health_check(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.anyio
async def test_recommend_known_patient(client):
    payload = {
        "patient_id": "p001",
        "context": {
            "meal_type": "lunch",
            "target_energy_kcal": 600,
            "target_protein_g": 25,
            "preferences": [],
            "allergies": [],
            "medical_conditions": [],
            "max_results": 3,
        },
    }
    response = await client.post("/api/v1/recommend/meals", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "p001"
    assert len(data["recommendations"]) <= 3
    assert data["method_used"] == "hybrid_ensemble (CBF 40% + CF 40% + Rules 20%)"


@pytest.mark.anyio
async def test_recommend_cold_start(client):
    payload = {
        "patient_id": "new_user",
        "context": {
            "meal_type": "breakfast",
            "target_energy_kcal": 350,
            "target_protein_g": 15,
            "preferences": ["low_carb"],
            "allergies": ["seafood"],
            "medical_conditions": ["diabetes"],
            "max_results": 3,
        },
    }
    response = await client.post("/api/v1/recommend/meals", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "new_user"
    assert "cold start" in data["method_used"]
    assert len(data["recommendations"]) <= 3


@pytest.mark.anyio
async def test_recommend_allergen_filtered(client):
    payload = {
        "patient_id": "p001",
        "context": {
            "meal_type": "lunch",
            "target_energy_kcal": 500,
            "target_protein_g": 20,
            "preferences": [],
            "allergies": ["seafood"],
            "medical_conditions": [],
            "max_results": 10,
        },
    }
    response = await client.post("/api/v1/recommend/meals", json=payload)
    data = response.json()
    food_names = [r["name"] for r in data["recommendations"]]
    for name in food_names:
        assert "udang" not in name.lower()


@pytest.mark.anyio
async def test_recommend_invalid_meal_type(client):
    payload = {
        "patient_id": "p001",
        "context": {
            "meal_type": "invalid_meal",
            "target_energy_kcal": 500,
            "target_protein_g": 20,
        },
    }
    response = await client.post("/api/v1/recommend/meals", json=payload)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_debug_filtered_foods(client):
    payload = {
        "patient_id": "test",
        "context": {
            "meal_type": "lunch",
            "target_energy_kcal": 500,
            "target_protein_g": 20,
            "preferences": ["low_carb"],
            "allergies": [],
            "medical_conditions": [],
            "max_results": 5,
        },
    }
    response = await client.post("/api/v1/debug/filtered-foods", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_input"] > 0