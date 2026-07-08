import pytest
from app.rules.constraints import ConstraintEngine, MEAL_TYPE_CATEGORIES, ALLERGEN_MAP, DIET_PREFERENCES, MEDICAL_CONDITIONS
from app.schemas.recommendation import RecommendationContext, MealType


@pytest.fixture
def sample_foods():
    return [
        {"food_id": "f001", "name": "Nasi Putih", "category": "nasi", "energy_kcal": 180, "protein_g": 3, "fat_g": 0.3, "carbs_g": 40, "fiber_g": 0.5, "serving_size_g": 100},
        {"food_id": "f002", "name": "Ikan Bakar", "category": "ikan", "energy_kcal": 150, "protein_g": 30, "fat_g": 3, "carbs_g": 0, "fiber_g": 0, "serving_size_g": 100},
        {"food_id": "f003", "name": "Udang Goreng", "category": "seafood", "energy_kcal": 200, "protein_g": 24, "fat_g": 10, "carbs_g": 5, "fiber_g": 0, "serving_size_g": 100},
        {"food_id": "f004", "name": "Es Krim", "category": "camilan", "energy_kcal": 250, "protein_g": 3, "fat_g": 15, "carbs_g": 28, "fiber_g": 0, "serving_size_g": 100},
    ]


def test_allergen_filter_seafood(sample_foods):
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=500, target_protein_g=20,
        allergies=["seafood"]
    )
    engine = ConstraintEngine(ctx)
    assert engine.apply_allergen_filter(sample_foods[2]) == False  # Udang category=seafood
    assert engine.apply_allergen_filter(sample_foods[1]) == True   # Ikan Bakar category=ikan


def test_allergen_filter_nuts():
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=500, target_protein_g=20,
        allergies=["nuts"]
    )
    engine = ConstraintEngine(ctx)
    assert engine.apply_allergen_filter({"name": "Kacang Tanah Goreng"}) == False
    assert engine.apply_allergen_filter({"name": "Ayam Goreng"}) == True


def test_diet_low_carb():
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=500, target_protein_g=20,
        preferences=["low_carb"]
    )
    engine = ConstraintEngine(ctx)
    assert engine.apply_diet_filter({"name": "Nasi", "carbs_g": 40}) == False
    assert engine.apply_diet_filter({"name": "Ikan", "carbs_g": 0}) == True


def test_diet_vegetarian():
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=500, target_protein_g=20,
        preferences=["vegetarian"]
    )
    engine = ConstraintEngine(ctx)
    assert engine.apply_diet_filter({"name": "Ayam", "category": "daging"}) == False
    assert engine.apply_diet_filter({"name": "Tempe", "category": "lauk"}) == True


def test_medical_diabetes():
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=500, target_protein_g=20,
        medical_conditions=["diabetes"]
    )
    engine = ConstraintEngine(ctx)
    assert engine.apply_medical_filter({"name": "Es Krim", "carbs_g": 35}) == False
    assert engine.apply_medical_filter({"name": "Ikan", "carbs_g": 0}) == True


def test_medical_ckd():
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=500, target_protein_g=20,
        medical_conditions=["ckd"]
    )
    engine = ConstraintEngine(ctx)
    assert engine.apply_medical_filter({"name": "Ikan", "protein_g": 30}) == False
    assert engine.apply_medical_filter({"name": "Nasi", "protein_g": 3}) == True


def test_medical_asam_urat():
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=500, target_protein_g=20,
        medical_conditions=["asam_urat"]
    )
    engine = ConstraintEngine(ctx)
    assert engine.apply_medical_filter({"name": "Hati Sapi", "category": "jeroan"}) == False
    assert engine.apply_medical_filter({"name": "Tahu", "category": "lauk"}) == True


def test_meal_type_breakfast():
    ctx = RecommendationContext(
        meal_type=MealType.breakfast, target_energy_kcal=300, target_protein_g=10
    )
    engine = ConstraintEngine(ctx)
    assert engine.apply_meal_type_filter({"name": "Bubur Ayam", "category": "bubur"}) == True
    assert engine.apply_meal_type_filter({"name": "Nasi Goreng", "category": "nasi"}) == False


def test_meal_type_snack():
    ctx = RecommendationContext(
        meal_type=MealType.snack, target_energy_kcal=150, target_protein_g=5
    )
    engine = ConstraintEngine(ctx)
    assert engine.apply_meal_type_filter({"name": "Pisang", "category": "buah"}) == True
    assert engine.apply_meal_type_filter({"name": "Soto Ayam", "category": "sup"}) == False


def test_full_filter_pipeline(sample_foods):
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=500, target_protein_g=20,
        allergies=["seafood"], preferences=["low_carb"], medical_conditions=["diabetes"]
    )
    engine = ConstraintEngine(ctx)
    filtered = engine.filter(sample_foods)
    assert len(filtered) >= 1
    assert all(f["food_id"] != "f003" for f in filtered)  # Udang difilter seafood


def test_score_rules_perfect_match():
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=200, target_protein_g=10,
        target_fat_g=5, target_carbs_g=20
    )
    engine = ConstraintEngine(ctx)
    food = {"energy_kcal": 200, "protein_g": 10, "fat_g": 5, "carbs_g": 20}
    score = engine.score_rules(food)
    assert score > 0.9


def test_score_rules_zero_target():
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=500, target_protein_g=0,
        target_fat_g=0, target_carbs_g=0
    )
    engine = ConstraintEngine(ctx)
    food = {"energy_kcal": 200, "protein_g": 10, "fat_g": 5, "carbs_g": 20}
    score = engine.score_rules(food)
    assert score > 0


def test_score_rules_clamped():
    ctx = RecommendationContext(
        meal_type=MealType.lunch, target_energy_kcal=100, target_protein_g=5
    )
    engine = ConstraintEngine(ctx)
    food = {"energy_kcal": 500, "protein_g": 50, "fat_g": 0, "carbs_g": 0}
    score = engine.score_rules(food)
    assert score <= 1.0
    assert score >= 0