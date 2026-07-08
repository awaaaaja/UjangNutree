import logging
import numpy as np
from app.models.hybrid import HybridRecommender
from app.schemas.recommendation import RecommendationContext, MealType

logger = logging.getLogger(__name__)


def evaluate(recommender: HybridRecommender) -> dict:
    test_cases = [
        {
            "patient_id": "p001",
            "context": RecommendationContext(
                meal_type=MealType.lunch,
                target_energy_kcal=600,
                target_protein_g=25,
                preferences=[],
                allergies=[],
                medical_conditions=[],
                max_results=5,
            ),
        },
        {
            "patient_id": "new_patient",
            "context": RecommendationContext(
                meal_type=MealType.breakfast,
                target_energy_kcal=350,
                target_protein_g=15,
                preferences=["low_carb"],
                allergies=["seafood"],
                medical_conditions=["diabetes"],
                max_results=3,
            ),
        },
        {
            "patient_id": "p002",
            "context": RecommendationContext(
                meal_type=MealType.dinner,
                target_energy_kcal=500,
                target_protein_g=20,
                preferences=["high_protein"],
                allergies=[],
                medical_conditions=[],
                max_results=5,
            ),
        },
    ]

    results = []
    for case in test_cases:
        recs = recommender.recommend(case["patient_id"], case["context"])
        results.append({
            "patient_id": case["patient_id"],
            "n_recommendations": len(recs),
            "scores": [r["score"] for r in recs],
            "food_names": [r["name"] for r in recs],
            "method": recommender.get_method_used(case["patient_id"]),
        })
        logger.info(
            f"Patient {case['patient_id']}: {len(recs)} recs, "
            f"method={results[-1]['method']}, "
            f"mean_score={np.mean(results[-1]['scores']):.3f}"
        )

    avg_results = np.mean([len(r["recommendations"]) if hasattr(r, "recommendations") else r["n_recommendations"] for r in results])

    logger.info(f"Evaluation complete. Avg recommendations per request: {avg_results:.1f}")
    return {"test_cases": results, "avg_recommendations": float(avg_results)}


if __name__ == "__main__":
    from train_pipeline import load_data, train_pipeline
    foods, interactions = load_data()
    model = train_pipeline(foods, interactions)
    metrics = evaluate(model)
    logger.info(f"Evaluation metrics: {metrics}")