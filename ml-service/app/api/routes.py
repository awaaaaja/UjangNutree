import logging
from fastapi import APIRouter, HTTPException
from app.schemas.recommendation import RecommendRequest, RecommendResponse, FoodRecommendation
from app.models.hybrid import HybridRecommender

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["recommendation"])

recommender = HybridRecommender()


def initialize_with_sample_data():
    sample_foods = [
        {"food_id": "f001", "name": "Nasi Putih", "category": "nasi", "energy_kcal": 180, "protein_g": 3, "fat_g": 0.3, "carbs_g": 40, "fiber_g": 0.5, "serving_size_g": 100},
        {"food_id": "f002", "name": "Ayam Goreng", "category": "lauk", "energy_kcal": 250, "protein_g": 25, "fat_g": 15, "carbs_g": 2, "fiber_g": 0, "serving_size_g": 100},
        {"food_id": "f003", "name": "Tempe Goreng", "category": "lauk", "energy_kcal": 200, "protein_g": 20, "fat_g": 10, "carbs_g": 8, "fiber_g": 2, "serving_size_g": 100},
        {"food_id": "f004", "name": "Sayur Bayam", "category": "sayur", "energy_kcal": 30, "protein_g": 3, "fat_g": 0.5, "carbs_g": 5, "fiber_g": 2, "serving_size_g": 100},
        {"food_id": "f005", "name": "Ikan Bakar", "category": "ikan", "energy_kcal": 150, "protein_g": 30, "fat_g": 3, "carbs_g": 0, "fiber_g": 0, "serving_size_g": 100},
        {"food_id": "f006", "name": "Telur Dadar", "category": "telur", "energy_kcal": 210, "protein_g": 14, "fat_g": 16, "carbs_g": 1, "fiber_g": 0, "serving_size_g": 100},
        {"food_id": "f007", "name": "Soto Ayam", "category": "sup", "energy_kcal": 180, "protein_g": 12, "fat_g": 8, "carbs_g": 15, "fiber_g": 1, "serving_size_g": 200},
        {"food_id": "f008", "name": "Gado-gado", "category": "sayur", "energy_kcal": 280, "protein_g": 8, "fat_g": 18, "carbs_g": 25, "fiber_g": 4, "serving_size_g": 200},
        {"food_id": "f009", "name": "Bubur Ayam", "category": "bubur", "energy_kcal": 160, "protein_g": 8, "fat_g": 4, "carbs_g": 25, "fiber_g": 0.5, "serving_size_g": 200},
        {"food_id": "f010", "name": "Pisang", "category": "buah", "energy_kcal": 105, "protein_g": 1, "fat_g": 0.4, "carbs_g": 27, "fiber_g": 3, "serving_size_g": 100},
        {"food_id": "f011", "name": "Susu Kambing", "category": "minuman", "energy_kcal": 130, "protein_g": 7, "fat_g": 8, "carbs_g": 10, "fiber_g": 0, "serving_size_g": 200},
        {"food_id": "f012", "name": "Apel", "category": "buah", "energy_kcal": 52, "protein_g": 0.3, "fat_g": 0.2, "carbs_g": 14, "fiber_g": 2.4, "serving_size_g": 100},
        {"food_id": "f013", "name": "Telur Rebus", "category": "telur", "energy_kcal": 155, "protein_g": 13, "fat_g": 11, "carbs_g": 1, "fiber_g": 0, "serving_size_g": 100},
        {"food_id": "f014", "name": "Tahu Goreng", "category": "lauk", "energy_kcal": 180, "protein_g": 12, "fat_g": 13, "carbs_g": 5, "fiber_g": 1, "serving_size_g": 100},
        {"food_id": "f015", "name": "Kentang Goreng", "category": "camilan", "energy_kcal": 312, "protein_g": 4, "fat_g": 15, "carbs_g": 42, "fiber_g": 3, "serving_size_g": 100},
        {"food_id": "f016", "name": "Udang Goreng", "category": "seafood", "energy_kcal": 200, "protein_g": 24, "fat_g": 10, "carbs_g": 5, "fiber_g": 0, "serving_size_g": 100},
        {"food_id": "f017", "name": "Cumi Goreng Tepung", "category": "seafood", "energy_kcal": 230, "protein_g": 18, "fat_g": 12, "carbs_g": 12, "fiber_g": 0, "serving_size_g": 100},
        {"food_id": "f018", "name": "Roti Gandum", "category": "roti", "energy_kcal": 250, "protein_g": 9, "fat_g": 3.5, "carbs_g": 45, "fiber_g": 6, "serving_size_g": 100},
        {"food_id": "f019", "name": "Overnight Oats", "category": "sereal", "energy_kcal": 200, "protein_g": 8, "fat_g": 5, "carbs_g": 34, "fiber_g": 5, "serving_size_g": 150},
        {"food_id": "f020", "name": "Salad Buah", "category": "buah", "energy_kcal": 120, "protein_g": 1, "fat_g": 0.5, "carbs_g": 30, "fiber_g": 3, "serving_size_g": 200},
    ]

    sample_interactions = [
        {"patient_id": "p001", "food_id": "f001", "rating": 4.5},
        {"patient_id": "p001", "food_id": "f002", "rating": 4.0},
        {"patient_id": "p001", "food_id": "f005", "rating": 5.0},
        {"patient_id": "p002", "food_id": "f001", "rating": 3.0},
        {"patient_id": "p002", "food_id": "f003", "rating": 4.5},
        {"patient_id": "p002", "food_id": "f004", "rating": 4.0},
        {"patient_id": "p003", "food_id": "f005", "rating": 5.0},
        {"patient_id": "p003", "food_id": "f006", "rating": 3.5},
        {"patient_id": "p003", "food_id": "f010", "rating": 4.0},
        {"patient_id": "p004", "food_id": "f002", "rating": 4.5},
        {"patient_id": "p004", "food_id": "f007", "rating": 4.0},
    ]

    recommender.fit_foods(sample_foods)
    recommender.fit_interactions(sample_interactions)
    logger.info(f"Initialized with {len(sample_foods)} foods and {len(sample_interactions)} interactions")


initialize_with_sample_data()


@router.post("/recommend/meals", response_model=RecommendResponse)
async def recommend_meals(request: RecommendRequest):
    try:
        recommendations = recommender.recommend(request.patient_id, request.context)
        method_used = recommender.get_method_used(request.patient_id)

        food_recs = [
            FoodRecommendation(
                food_id=r["food_id"],
                name=r["name"],
                category=r.get("category", ""),
                energy_kcal=r.get("energy_kcal", 0),
                protein_g=r.get("protein_g", 0),
                fat_g=r.get("fat_g", 0),
                carbs_g=r.get("carbs_g", 0),
                fiber_g=r.get("fiber_g", 0),
                serving_size_g=r.get("serving_size_g", 100),
                score=r["score"],
                reason=r["reason"],
            )
            for r in recommendations
        ]

        return RecommendResponse(
            patient_id=request.patient_id,
            recommendations=food_recs,
            method_used=method_used,
            total_candidates=len(recommendations),
        )
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": recommender._fitted}


@router.post("/debug/filtered-foods")
async def debug_filtered_foods(request: RecommendRequest):
    from app.rules.constraints import ConstraintEngine
    engine = ConstraintEngine(request.context)
    filtered = engine.filter(recommender.foods)
    return {
        "total_input": len(recommender.foods),
        "total_filtered": len(filtered),
        "foods": filtered,
    }