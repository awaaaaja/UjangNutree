from app.schemas.recommendation import RecommendationContext, MealType

ALLERGEN_MAP = {
    "seafood": ["seafood", "udang", "kepiting", "cumi", "kerang"],
    "nuts": ["kacang", "almond", "walnut", "cashew"],
    "dairy": ["susu", "keju", "yogurt", "cream"],
    "gluten": ["terigu", "gandum", "roti", "pasta", "mie"],
    "egg": ["telur"],
    "soy": ["kedelai", "tahu", "tempe"],
}

DIET_PREFERENCES = {
    "low_carb": {"max_carbs_per_serving": 20},
    "high_protein": {"min_protein_per_serving": 15},
    "low_fat": {"max_fat_per_serving": 10},
    "vegetarian": {"exclude_categories": ["daging", "ayam", "ikan", "seafood"]},
    "vegan": {"exclude_categories": ["daging", "ayam", "ikan", "seafood", "susu", "telur"]},
}

MEDICAL_CONDITIONS = {
    "diabetes": {"max_carbs_per_serving": 30, "max_sugar_per_serving": 10},
    "hipertensi": {"max_sodium_mg": 600},
    "ckd": {"max_protein_per_serving": 10, "max_sodium_mg": 400, "max_kalium_mg": 300},
    "asam_urat": {"exclude_categories": ["jeroan", "seafood", "daging_merah"]},
    "maag": {"exclude_categories": ["pedas", "asam", "bersantan"]},
}

MEAL_TYPE_CATEGORIES = {
    MealType.breakfast: ["sereal", "roti", "buah", "susu", "telur", "bubur"],
    MealType.lunch: ["nasi", "lauk", "sayur", "daging", "ayam", "ikan"],
    MealType.dinner: ["nasi", "lauk", "sayur", "sup", "daging", "ayam", "ikan"],
    MealType.snack: ["buah", "kue", "camilan", "minuman"],
}


class ConstraintEngine:
    def __init__(self, context: RecommendationContext):
        self.context = context

    def apply_allergen_filter(self, food: dict) -> bool:
        food_category = food.get("category", "").lower()
        food_name = food.get("name", "").lower()
        for allergen in self.context.allergies:
            keywords = ALLERGEN_MAP.get(allergen, [allergen])
            if food_category in keywords:
                return False
            for kw in keywords:
                if kw in food_name:
                    return False
        return True

    def apply_diet_filter(self, food: dict) -> bool:
        for pref in self.context.preferences:
            rules = DIET_PREFERENCES.get(pref)
            if not rules:
                continue
            if "max_carbs_per_serving" in rules:
                if food.get("carbs_g", 0) > rules["max_carbs_per_serving"]:
                    return False
            if "min_protein_per_serving" in rules:
                if food.get("protein_g", 0) < rules["min_protein_per_serving"]:
                    return False
            if "max_fat_per_serving" in rules:
                if food.get("fat_g", 0) > rules["max_fat_per_serving"]:
                    return False
            if "exclude_categories" in rules:
                if food.get("category", "") in rules["exclude_categories"]:
                    return False
        return True

    def apply_medical_filter(self, food: dict) -> bool:
        for condition in self.context.medical_conditions:
            rules = MEDICAL_CONDITIONS.get(condition)
            if not rules:
                continue
            if "max_carbs_per_serving" in rules:
                if food.get("carbs_g", 0) > rules["max_carbs_per_serving"]:
                    return False
            if "max_protein_per_serving" in rules:
                if food.get("protein_g", 0) > rules["max_protein_per_serving"]:
                    return False
            if "exclude_categories" in rules:
                if food.get("category", "") in rules["exclude_categories"]:
                    return False
        return True

    def apply_meal_type_filter(self, food: dict) -> bool:
        allowed = MEAL_TYPE_CATEGORIES.get(self.context.meal_type, [])
        if not allowed:
            return True
        food_cat = food.get("category", "").lower()
        for a in allowed:
            if a in food_cat:
                return True
        return False

    def get_max_results(self) -> int:
        return self.context.max_results

    def filter(self, foods: list[dict]) -> list[dict]:
        filtered = []
        for f in foods:
            if not self.apply_allergen_filter(f):
                continue
            if not self.apply_diet_filter(f):
                continue
            if not self.apply_medical_filter(f):
                continue
            if not self.apply_meal_type_filter(f):
                continue
            filtered.append(f)
        return filtered

    def score_rules(self, food: dict) -> float:
        score = 0.0
        target = self.context

        energy_ratio = min(food.get("energy_kcal", 0) / target.target_energy_kcal, 2.0) if target.target_energy_kcal > 0 else 0
        score += max(0, 1 - abs(1 - energy_ratio)) * 0.5

        if target.target_protein_g > 0:
            protein_ratio = min(food.get("protein_g", 0) / target.target_protein_g, 2.0)
            score += max(0, 1 - abs(1 - protein_ratio)) * 0.3

        if target.target_fat_g > 0:
            fat_ratio = min(food.get("fat_g", 0) / target.target_fat_g, 2.0)
            score += max(0, 1 - abs(1 - fat_ratio)) * 0.1

        if target.target_carbs_g > 0:
            carbs_ratio = min(food.get("carbs_g", 0) / target.target_carbs_g, 2.0)
            score += max(0, 1 - abs(1 - carbs_ratio)) * 0.1

        return min(score, 1.0)