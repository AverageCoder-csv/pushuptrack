import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os

# Challenge types and their requirements
CHALLENGE_TYPES = {
    "Daily Push": {
        "description": "Complete target number of pushups in one day",
        "duration": 1,  # days
        "points": 100
    },
    "Weekly Warrior": {
        "description": "Achieve total pushup goal over a week",
        "duration": 7,
        "points": 300
    },
    "Variety Master": {
        "description": "Complete pushups using specified number of variations",
        "duration": 3,
        "points": 200
    },
    "Endurance Test": {
        "description": "Complete daily pushups for consecutive days",
        "duration": 5,
        "points": 250
    }
}

# Challenge badges and their criteria
CHALLENGE_BADGES = {
    "Bronze Challenger": {"min_points": 500, "icon": "🥉"},
    "Silver Champion": {"min_points": 1000, "icon": "🥈"},
    "Gold Master": {"min_points": 2000, "icon": "🥇"},
    "Diamond Elite": {"min_points": 5000, "icon": "💎"}
}

class SocialChallenges:
    def __init__(self):
        self.challenges_file = "data/challenges.json"
        self.leaderboard_file = "data/leaderboard.json"
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Create data files if they don't exist."""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.challenges_file):
            self._save_challenges({})
        if not os.path.exists(self.leaderboard_file):
            self._save_leaderboard({})

    def _load_challenges(self) -> Dict:
        """Load challenges from JSON file."""
        with open(self.challenges_file, 'r') as f:
            return json.load(f)

    def _save_challenges(self, challenges: Dict):
        """Save challenges to JSON file."""
        with open(self.challenges_file, 'w') as f:
            json.dump(challenges, f, indent=2)

    def _load_leaderboard(self) -> Dict:
        """Load leaderboard data from JSON file."""
        with open(self.leaderboard_file, 'r') as f:
            return json.load(f)

    def _save_leaderboard(self, leaderboard: Dict):
        """Save leaderboard data to JSON file."""
        with open(self.leaderboard_file, 'w') as f:
            json.dump(leaderboard, f, indent=2)

    def create_challenge(self, name: str, challenge_type: str, target: int, start_date: str) -> Dict:
        """Create a new challenge."""
        if challenge_type not in CHALLENGE_TYPES:
            raise ValueError(f"Invalid challenge type. Must be one of {list(CHALLENGE_TYPES.keys())}")

        challenges = self._load_challenges()
        new_challenge = {
            "name": name,
            "type": challenge_type,
            "target": target,
            "start_date": start_date,
            "duration": CHALLENGE_TYPES[challenge_type]["duration"],
            "points": CHALLENGE_TYPES[challenge_type]["points"],
            "participants": {},
            "status": "active"
        }
        
        challenges[name] = new_challenge
        self._save_challenges(challenges)
        return new_challenge

    def join_challenge(self, challenge_name: str, user_id: str):
        """Join a challenge."""
        challenges = self._load_challenges()
        if challenge_name not in challenges:
            raise ValueError("Challenge not found")

        if challenges[challenge_name]["status"] != "active":
            raise ValueError("Challenge is not active")

        if user_id not in challenges[challenge_name]["participants"]:
            challenges[challenge_name]["participants"][user_id] = {
                "progress": 0,
                "completed": False,
                "join_date": datetime.now().strftime("%Y-%m-%d")
            }
            self._save_challenges(challenges)

    def update_progress(self, challenge_name: str, user_id: str, progress: int):
        """Update user's progress in a challenge."""
        challenges = self._load_challenges()
        if challenge_name not in challenges:
            raise ValueError("Challenge not found")

        if user_id not in challenges[challenge_name]["participants"]:
            raise ValueError("User not participating in challenge")

        challenges[challenge_name]["participants"][user_id]["progress"] = progress
        if progress >= challenges[challenge_name]["target"]:
            challenges[challenge_name]["participants"][user_id]["completed"] = True
            self._award_points(user_id, challenges[challenge_name]["points"])

        self._save_challenges(challenges)

    def _award_points(self, user_id: str, points: int):
        """Award points to a user and update leaderboard."""
        leaderboard = self._load_leaderboard()
        if user_id not in leaderboard:
            leaderboard[user_id] = {"points": 0, "badges": []}
        
        leaderboard[user_id]["points"] += points
        
        # Check for new badges
        current_points = leaderboard[user_id]["points"]
        for badge, criteria in CHALLENGE_BADGES.items():
            if current_points >= criteria["min_points"] and badge not in leaderboard[user_id]["badges"]:
                leaderboard[user_id]["badges"].append(badge)
        
        self._save_leaderboard(leaderboard)

    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users from leaderboard."""
        leaderboard = self._load_leaderboard()
        sorted_users = sorted(
            [{"user_id": k, **v} for k, v in leaderboard.items()],
            key=lambda x: x["points"],
            reverse=True
        )
        return sorted_users[:limit]

    def get_active_challenges(self) -> List[Dict]:
        """Get list of active challenges."""
        challenges = self._load_challenges()
        return [
            {**challenge, "name": name}
            for name, challenge in challenges.items()
            if challenge["status"] == "active"
        ]

    def get_user_challenges(self, user_id: str) -> List[Dict]:
        """Get challenges for a specific user."""
        challenges = self._load_challenges()
        return [
            {**challenge, "name": name}
            for name, challenge in challenges.items()
            if user_id in challenge["participants"]
        ]

    def get_user_stats(self, user_id: str) -> Dict:
        """Get user's challenge statistics and badges."""
        leaderboard = self._load_leaderboard()
        if user_id not in leaderboard:
            return {"points": 0, "badges": [], "rank": None}
        
        # Calculate user's rank
        sorted_users = sorted(
            leaderboard.items(),
            key=lambda x: x[1]["points"],
            reverse=True
        )
        rank = next(i for i, (uid, _) in enumerate(sorted_users, 1) if uid == user_id)
        
        return {
            **leaderboard[user_id],
            "rank": rank
        }
