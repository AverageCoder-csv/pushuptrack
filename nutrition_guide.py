import math
from typing import Dict, Tuple

def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation."""
    if gender.lower() == "male":
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        return (10 * weight) + (6.25 * height) - (5 * age) - 161

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Calculate Total Daily Energy Expenditure."""
    activity_multipliers = {
        "sedentary": 1.2,      # Little or no exercise
        "light": 1.375,        # Light exercise 1-3 days/week
        "moderate": 1.55,      # Moderate exercise 3-5 days/week
        "active": 1.725,       # Heavy exercise 6-7 days/week
        "very_active": 1.9     # Very heavy exercise, physical job
    }
    return bmr * activity_multipliers[activity_level]

def calculate_macros(calories: float, goal: str) -> Dict[str, float]:
    """Calculate macro breakdown based on fitness goal."""
    if goal == "bulk":
        protein_ratio = 0.25  # 25% of calories from protein
        fat_ratio = 0.25     # 25% of calories from fat
        carb_ratio = 0.50    # 50% of calories from carbs
    elif goal == "cut":
        protein_ratio = 0.40  # 40% of calories from protein
        fat_ratio = 0.25     # 25% of calories from fat
        carb_ratio = 0.35    # 35% of calories from carbs
    else:  # maintenance
        protein_ratio = 0.30  # 30% of calories from protein
        fat_ratio = 0.25     # 25% of calories from fat
        carb_ratio = 0.45    # 45% of calories from carbs

    protein_cals = calories * protein_ratio
    fat_cals = calories * fat_ratio
    carb_cals = calories * carb_ratio

    return {
        "protein": round(protein_cals / 4),  # 4 calories per gram of protein
        "fats": round(fat_cals / 9),         # 9 calories per gram of fat
        "carbs": round(carb_cals / 4)        # 4 calories per gram of carbs
    }

MEAL_SUGGESTIONS = {
    "bulk": {
        "breakfast": [
            "Oatmeal with protein powder, banana, and peanut butter",
            "Whole grain toast with eggs and avocado",
            "Greek yogurt parfait with granola and berries"
        ],
        "lunch": [
            "Chicken breast with brown rice and vegetables",
            "Tuna sandwich with whole grain bread",
            "Turkey and quinoa bowl with mixed vegetables"
        ],
        "dinner": [
            "Lean beef stir-fry with rice",
            "Salmon with sweet potato and broccoli",
            "Pasta with turkey meatballs and sauce"
        ],
        "snacks": [
            "Protein shake with banana",
            "Mixed nuts and dried fruits",
            "Greek yogurt with honey"
        ]
    },
    "cut": {
        "breakfast": [
            "Egg white omelet with vegetables",
            "Protein smoothie with spinach",
            "Greek yogurt with berries"
        ],
        "lunch": [
            "Grilled chicken salad",
            "Tuna with mixed greens",
            "Turkey lettuce wraps"
        ],
        "dinner": [
            "White fish with vegetables",
            "Chicken breast with asparagus",
            "Tofu stir-fry with cauliflower rice"
        ],
        "snacks": [
            "Protein shake",
            "Celery with peanut butter",
            "Hard-boiled eggs"
        ]
    }
}

def get_meal_plan(goal: str) -> Dict:
    """Get meal suggestions based on fitness goal."""
    return MEAL_SUGGESTIONS.get(goal, MEAL_SUGGESTIONS["bulk"])

def calculate_nutrition_plan(
    weight: float,
    height: float,
    age: int,
    gender: str,
    activity_level: str,
    goal: str
) -> Dict:
    """Calculate complete nutrition plan."""
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    
    # Adjust calories based on goal
    if goal == "bulk":
        target_calories = tdee + 500  # Caloric surplus for bulking
    elif goal == "cut":
        target_calories = tdee - 500  # Caloric deficit for cutting
    else:
        target_calories = tdee
    
    macros = calculate_macros(target_calories, goal)
    meal_suggestions = get_meal_plan(goal)
    
    return {
        "target_calories": round(target_calories),
        "macros": macros,
        "meal_suggestions": meal_suggestions
    }
