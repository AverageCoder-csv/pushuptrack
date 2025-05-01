# Difficulty level multipliers
DIFFICULTY_LEVELS = {
    "Easy": 0.7,
    "Normal": 1.0,
    "Hard": 1.3,
    "Expert": 1.6
}

# Pushup variations with descriptions
PUSHUP_VARIATIONS = {
    "Wall": {
        "description": "Standing pushups against a wall - perfect for absolute beginners",
        "difficulty": 0.3,
        "beginner_friendly": True
    },
    "Knee": {
        "description": "Modified pushup performed on knees, great for building initial strength",
        "difficulty": 0.5,
        "beginner_friendly": True
    },
    "Incline": {
        "description": "Hands elevated on a stable surface, easier than standard pushups",
        "difficulty": 0.7,
        "beginner_friendly": True
    },
    "Standard": {
        "description": "Traditional pushup with hands shoulder-width apart",
        "difficulty": 1.0,
        "beginner_friendly": True
    },
    "Close Grip": {
        "description": "Hands closer than shoulder width, emphasizing triceps",
        "difficulty": 1.1,
        "beginner_friendly": True
    },
    "Wide Grip": {
        "description": "Hands placed wider than shoulder-width, focuses on chest",
        "difficulty": 1.2,
        "beginner_friendly": False
    },
    "Diamond": {
        "description": "Hands close together forming a diamond, focuses on triceps",
        "difficulty": 1.4,
        "beginner_friendly": False
    },
    "Decline": {
        "description": "Feet elevated, increasing upper chest engagement",
        "difficulty": 1.3,
        "beginner_friendly": False
    },
    "Staggered": {
        "description": "One hand slightly forward, the other back",
        "difficulty": 1.3,
        "beginner_friendly": False
    },
    "Pike": {
        "description": "Body in an inverted V-shape, targeting shoulders",
        "difficulty": 1.4,
        "beginner_friendly": False
    },
    "Deficit": {
        "description": "Hands on elevated surfaces for deeper range of motion",
        "difficulty": 1.5,
        "beginner_friendly": False
    },
    "Archer": {
        "description": "One arm slides out while the other stays fixed",
        "difficulty": 1.7,
        "beginner_friendly": False
    },
    "Spiderman": {
        "description": "Bring alternate knees to elbows during the movement",
        "difficulty": 1.6,
        "beginner_friendly": False
    },
    "Shoulder Tap": {
        "description": "Tap opposite shoulder at the top of each rep",
        "difficulty": 1.5,
        "beginner_friendly": False
    },
    "Hand Release": {
        "description": "Lift hands off ground at bottom of each rep",
        "difficulty": 1.3,
        "beginner_friendly": False
    },
    "Offset": {
        "description": "One hand on elevated surface, other on ground",
        "difficulty": 1.4,
        "beginner_friendly": False
    },
    "Leg Raise": {
        "description": "Raise one leg during the pushup",
        "difficulty": 1.4,
        "beginner_friendly": False
    },
    "Weighted": {
        "description": "Additional weight on back for increased difficulty",
        "difficulty": 1.8,
        "beginner_friendly": False
    },
    "Clap": {
        "description": "Explosive movement with clap at top",
        "difficulty": 1.8,
        "beginner_friendly": False
    },
    "Plyo": {
        "description": "Explosive push-up with hands leaving ground",
        "difficulty": 1.9,
        "beginner_friendly": False
    },
    "Superman": {
        "description": "Arms extended forward at top like Superman flying",
        "difficulty": 2.0,
        "beginner_friendly": False
    },
    "Narrow": {
        "description": "Hands closer than shoulder width, harder than close grip",
        "difficulty": 1.5,
        "beginner_friendly": False
    },
    "One-Handed": {
        "description": "Ultimate challenge - pushup using single arm",
        "difficulty": 2.5,
        "beginner_friendly": False
    }
}

BASE_WORKOUT_PLANS = {
    "Beginner 30-Day Challenge": [
        {"day": 1, "target": 5, "type": "Wall"},
        {"day": 2, "target": 6, "type": "Wall"},
        {"day": 3, "target": 7, "type": "Knee"},
        {"day": 4, "target": 8, "type": "Wall"},
        {"day": 5, "target": 9, "type": "Knee"},
        {"day": 6, "target": "Rest", "type": "Rest"},
        {"day": 7, "target": 10, "type": "Incline"},
        {"day": 8, "target": 11, "type": "Knee"},
        {"day": 9, "target": 12, "type": "Incline"},
        {"day": 10, "target": 13, "type": "Standard"},
        {"day": 11, "target": 14, "type": "Knee"},
        {"day": 12, "target": 15, "type": "Incline"},
        {"day": 13, "target": 16, "type": "Standard"},
        {"day": 14, "target": 17, "type": "Standard"},
        {"day": 15, "target": 18, "type": "Close Grip"},
        {"day": 16, "target": 19, "type": "Standard"},
        {"day": 17, "target": 20, "type": "Close Grip"},
        {"day": 18, "target": 21, "type": "Standard"},
        {"day": 19, "target": 22, "type": "Wide Grip"},
        {"day": 20, "target": 23, "type": "Standard"},
        {"day": 21, "target": "Rest", "type": "Rest"},
        {"day": 22, "target": 25, "type": "Standard"},
        {"day": 23, "target": 26, "type": "Close Grip"},
        {"day": 24, "target": 27, "type": "Wide Grip"},
        {"day": 25, "target": 28, "type": "Standard"},
        {"day": 26, "target": 29, "type": "Wide Grip"},
        {"day": 27, "target": 30, "type": "Standard"},
        {"day": 28, "target": 25, "type": "Diamond"},
        {"day": 29, "target": 28, "type": "Standard"},
        {"day": 30, "target": 30, "type": "Wide Grip"}
    ],
    "Intermediate 30-Day Challenge": [
        {"day": 1, "target": 15, "type": "Standard"},
        {"day": 2, "target": 17, "type": "Wide Grip"},
        {"day": 3, "target": 19, "type": "Diamond"},
        {"day": 4, "target": 21, "type": "Decline"},
        {"day": 5, "target": 23, "type": "Close Grip"},
        {"day": 6, "target": "Rest", "type": "Rest"},
        {"day": 7, "target": 25, "type": "Standard"},
        {"day": 8, "target": 27, "type": "Staggered"},
        {"day": 9, "target": 29, "type": "Pike"},
        {"day": 10, "target": 31, "type": "Hand Release"},
        {"day": 11, "target": 33, "type": "Deficit"},
        {"day": 12, "target": 35, "type": "Shoulder Tap"},
        {"day": 13, "target": 37, "type": "Spiderman"},
        {"day": 14, "target": "Rest", "type": "Rest"},
        {"day": 15, "target": 41, "type": "Standard"},
        {"day": 16, "target": 43, "type": "Archer"},
        {"day": 17, "target": 45, "type": "Clap"},
        {"day": 18, "target": 47, "type": "Leg Raise"},
        {"day": 19, "target": 49, "type": "Weighted"},
        {"day": 20, "target": 51, "type": "Plyo"},
        {"day": 21, "target": "Rest", "type": "Rest"},
        {"day": 22, "target": 55, "type": "Superman"},
        {"day": 23, "target": 57, "type": "One-Handed"},
        {"day": 24, "target": 59, "type": "Standard"},
        {"day": 25, "target": 61, "type": "Archer"},
        {"day": 26, "target": 63, "type": "Plyo"},
        {"day": 27, "target": 65, "type": "Standard"},
        {"day": 28, "target": 45, "type": "One-Handed"},
        {"day": 29, "target": 48, "type": "Weighted"},
        {"day": 30, "target": 50, "type": "Superman"}
    ]
}

def get_adjusted_workout_plan(plan_name: str, difficulty: str) -> list:
    """
    Adjust workout plan based on selected difficulty level.
    """
    base_plan = BASE_WORKOUT_PLANS[plan_name]
    multiplier = DIFFICULTY_LEVELS[difficulty]

    adjusted_plan = []
    for day in base_plan:
        if day["target"] == "Rest":
            adjusted_plan.append({"day": day["day"], "target": "Rest", "type": "Rest"})
        else:
            adjusted_target = round(day["target"] * multiplier)
            adjusted_plan.append({
                "day": day["day"], 
                "target": adjusted_target,
                "type": day["type"]
            })

    return adjusted_plan

MOTIVATIONAL_MESSAGES = [
    "Every pushup makes you stronger! 💪",
    "You're crushing it! Keep going! 🚀",
    "Small progress is still progress! 🌱",
    "Stay consistent, stay strong! 🎯",
    "You're building a better you! 🏆",
    "Don't stop now, you're doing great! ⭐",
]

ACHIEVEMENTS = {
    "Beginner": {"requirement": 100, "description": "Complete 100 total pushups"},
    "Intermediate": {"requirement": 500, "description": "Complete 500 total pushups"},
    "Advanced": {"requirement": 1000, "description": "Complete 1000 total pushups"},
    "Consistency King": {"requirement": 7, "description": "Log pushups for 7 consecutive days"},
    "Push-up Master": {"requirement": 50, "description": "Complete 50 pushups in one day"}
}