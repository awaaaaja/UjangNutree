from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class MealType(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"


class RecommendationContext(BaseModel):
    meal_type: MealType
    target_energy_kcal: float = Field(..., gt=0)
    target_protein_g: float = Field(..., ge=0)
    target_fat_g: float = Field(default=0, ge=0)
    target_carbs_g: float = Field(default=0, ge=0)
    preferences: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    medical_conditions: list[str] = Field(default_factory=list)
    max_results: int = Field(default=5, ge=1, le=50)


class RecommendRequest(BaseModel):
    patient_id: str
    context: RecommendationContext


class FoodRecommendation(BaseModel):
    food_id: str
    name: str
    category: str
    energy_kcal: float
    protein_g: float
    fat_g: float
    carbs_g: float
    fiber_g: float
    serving_size_g: float
    score: float
    reason: str


class RecommendResponse(BaseModel):
    patient_id: str
    recommendations: list[FoodRecommendation]
    method_used: str
    total_candidates: int