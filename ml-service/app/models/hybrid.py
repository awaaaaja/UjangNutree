from app.models.cbf import ContentBasedFiltering
from app.models.cf import CollaborativeFiltering
from app.rules.constraints import ConstraintEngine
from app.schemas.recommendation import RecommendationContext
from typing import Optional


class HybridRecommender:
    CBF_WEIGHT = 0.4
    CF_WEIGHT = 0.4
    RULE_WEIGHT = 0.2

    def __init__(self):
        self.cbf = ContentBasedFiltering()
        self.cf = CollaborativeFiltering()
        self.foods: list[dict] = []
        self._fitted = False

    def fit_foods(self, foods: list[dict]):
        self.foods = foods
        self.cbf.fit(foods)

    def fit_interactions(self, interactions: list[dict]):
        self.cf.fit(interactions)
        self._fitted = True

    def recommend(self, patient_id: str, context: RecommendationContext) -> list[dict]:
        engine = ConstraintEngine(context)
        filtered_foods = engine.filter(self.foods)

        cbf_weight = self.CBF_WEIGHT
        cf_weight = self.CF_WEIGHT

        user_has_history = patient_id in self.cf.user_map
        is_new_patient = not user_has_history

        if is_new_patient:
            cf_weight = 0.0
            cbf_weight = 0.6
        elif len(filtered_foods) < 20:
            cf_weight = 0.2
            cbf_weight = 0.6

        if self.cf._fitted and user_has_history:
            cf_results = self.cf.recommend(patient_id, top_k=50)
            cf_scores = {r["food_id"]: r["score"] for r in cf_results}
        else:
            cf_scores = {}

        if is_new_patient:
            target = {
                "energy_kcal": context.target_energy_kcal,
                "protein_g": context.target_protein_g,
                "fat_g": context.target_fat_g or context.target_energy_kcal * 0.25 / 9,
                "carbs_g": context.target_carbs_g or context.target_energy_kcal * 0.55 / 4,
                "fiber_g": 0,
            }
            cbf_results = self.cbf.recommend_by_profile(target, top_k=50)
        else:
            cold_start_foods = [f for f in filtered_foods if f["food_id"] not in self.cf.item_map]
            known_foods = [f for f in filtered_foods if f["food_id"] in self.cf.item_map]

            cbf_results = []
            for f in known_foods[:1]:
                cbf_results.extend(self.cbf.recommend(f["food_id"], top_k=30))
            for f in cold_start_foods[:10]:
                cbf_results.append({**f, "score": 0.3, "reason": "cold start"})

        cbf_scores = {}
        for r in cbf_results:
            fid = r["food_id"]
            cbf_scores[fid] = max(cbf_scores.get(fid, 0), r["score"])

        scored = []
        for food in filtered_foods:
            fid = food["food_id"]
            cbf_score = cbf_scores.get(fid, 0)
            cf_score = cf_scores.get(fid, 0)
            rule_score = engine.score_rules(food)

            hybrid_score = (
                cbf_score * cbf_weight +
                cf_score * cf_weight +
                rule_score * self.RULE_WEIGHT
            )

            if hybrid_score > 0:
                scored.append({
                    **food,
                    "score": round(hybrid_score, 4),
                    "reason": (
                        f"CBF: {cbf_score:.2f}, CF: {cf_score:.2f}, Rules: {rule_score:.2f}"
                    )
                })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:context.max_results]

    def get_method_used(self, patient_id: str) -> str:
        is_new = patient_id not in self.cf.user_map
        if is_new:
            return "cbf_profile_based (cold start)"
        return "hybrid_ensemble (CBF 40% + CF 40% + Rules 20%)"