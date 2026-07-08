import json
import logging
import mlflow
from pathlib import Path
from app.models.cbf import ContentBasedFiltering
from app.models.cf import CollaborativeFiltering
from app.models.hybrid import HybridRecommender

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(data_dir: str = "data") -> tuple[list[dict], list[dict]]:
    data_path = Path(data_dir)
    foods_path = data_path / "foods.json"
    interactions_path = data_path / "interactions.json"

    foods = json.loads(foods_path.read_text()) if foods_path.exists() else []
    interactions = json.loads(interactions_path.read_text()) if interactions_path.exists() else []

    logger.info(f"Loaded {len(foods)} foods and {len(interactions)} interactions")
    return foods, interactions


def train_pipeline(foods: list[dict], interactions: list[dict]) -> HybridRecommender:
    mlflow.set_experiment("UjangNutree_Recommendation")

    with mlflow.start_run():
        cbf = ContentBasedFiltering()
        cbf.fit(foods)
        logger.info("CBF model trained")

        cf = CollaborativeFiltering(n_factors=20, n_epochs=50)
        cf.fit(interactions)
        logger.info("CF model trained")

        hybrid = HybridRecommender()
        hybrid.cbf = cbf
        hybrid.cf = cf
        hybrid.foods = foods
        hybrid._fitted = True

        mlflow.log_param("n_foods", len(foods))
        mlflow.log_param("n_interactions", len(interactions))
        mlflow.log_param("n_users", len(set(i["patient_id"] for i in interactions)))
        mlflow.log_param("n_items_cf", len(cf.item_map))

        logger.info("Hybrid model ready")
        return hybrid


if __name__ == "__main__":
    foods, interactions = load_data()
    model = train_pipeline(foods, interactions)
    logger.info(f"Model trained with {model.get_method_used('test')}")