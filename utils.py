import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Tuple
import random
from workout_plans import MOTIVATIONAL_MESSAGES, ACHIEVEMENTS

DATA_FILE = "data/pushup_data.csv"

def ensure_data_file_exists():
    """Ensure the data file exists and has the correct structure."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=['date', 'pushups', 'type'])
        df.to_csv(DATA_FILE, index=False)

def load_data() -> pd.DataFrame:
    """Load pushup data from CSV file."""
    ensure_data_file_exists()
    df = pd.read_csv(DATA_FILE)
    df['date'] = pd.to_datetime(df['date'])
    if 'type' not in df.columns:
        df['type'] = 'Standard'  # Add type column for backward compatibility
    return df

def save_pushups(date: str, count: int, pushup_type: str = "Standard"):
    """Save pushup data to CSV file."""
    df = load_data()

    # Convert string date to datetime
    date_obj = pd.to_datetime(date)

    # Check if entry for this date already exists
    if not df[df['date'] == date_obj].empty:
        df.loc[df['date'] == date_obj, 'pushups'] = count
        df.loc[df['date'] == date_obj, 'type'] = pushup_type
    else:
        new_row = pd.DataFrame({
            'date': [date_obj], 
            'pushups': [count],
            'type': [pushup_type]
        })
        df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(DATA_FILE, index=False)

def get_statistics(df: pd.DataFrame) -> Dict:
    """Calculate various statistics from the pushup data."""
    if df.empty:
        return {
            "total_pushups": 0,
            "daily_average": 0,
            "best_day": None,
            "current_streak": 0,
            "longest_streak": 0,
            "type_breakdown": {}
        }

    total_pushups = df['pushups'].sum()
    daily_average = round(df['pushups'].mean(), 1)
    best_day = df.loc[df['pushups'].idxmax()]

    # Calculate streaks
    df_sorted = df.sort_values('date')
    current_streak, longest_streak = calculate_streaks(df_sorted)

    # Calculate pushup type breakdown
    type_breakdown = df.groupby('type')['pushups'].sum().to_dict()

    return {
        "total_pushups": total_pushups,
        "daily_average": daily_average,
        "best_day": best_day,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "type_breakdown": type_breakdown
    }

def calculate_streaks(df: pd.DataFrame) -> Tuple[int, int]:
    """Calculate current and longest streaks."""
    if df.empty:
        return 0, 0

    # Convert dates to datetime if they aren't already
    df['date'] = pd.to_datetime(df['date'])

    # Sort by date
    df = df.sort_values('date')

    # Calculate date differences
    date_diffs = df['date'].diff().dt.days

    # Initialize streak variables
    current_streak = 1
    longest_streak = 1
    temp_streak = 1

    # Calculate streaks
    for diff in date_diffs:
        if diff == 1:  # consecutive days
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1

    # Calculate current streak
    today = pd.Timestamp.now().date()
    if df['date'].iloc[-1].date() == today:
        current_streak = temp_streak
    else:
        current_streak = 0

    return current_streak, longest_streak

def get_random_motivation() -> str:
    """Return a random motivational message."""
    return random.choice(MOTIVATIONAL_MESSAGES)

def check_achievements(stats: Dict) -> List[Dict]:
    """Check which achievements have been unlocked."""
    unlocked = []

    # Check total pushups achievements
    if stats["total_pushups"] >= ACHIEVEMENTS["Beginner"]["requirement"]:
        unlocked.append({"name": "Beginner", **ACHIEVEMENTS["Beginner"]})
    if stats["total_pushups"] >= ACHIEVEMENTS["Intermediate"]["requirement"]:
        unlocked.append({"name": "Intermediate", **ACHIEVEMENTS["Intermediate"]})
    if stats["total_pushups"] >= ACHIEVEMENTS["Advanced"]["requirement"]:
        unlocked.append({"name": "Advanced", **ACHIEVEMENTS["Advanced"]})

    # Check streak achievement
    if stats["current_streak"] >= ACHIEVEMENTS["Consistency King"]["requirement"]:
        unlocked.append({"name": "Consistency King", **ACHIEVEMENTS["Consistency King"]})

    # Check daily max achievement
    df = load_data()
    if not df.empty and df['pushups'].max() >= ACHIEVEMENTS["Push-up Master"]["requirement"]:
        unlocked.append({"name": "Push-up Master", **ACHIEVEMENTS["Push-up Master"]})

    return unlocked

def get_weekly_statistics(df: pd.DataFrame) -> Dict:
    """Calculate detailed weekly statistics."""
    if df.empty:
        return {
            "current_week_total": 0,
            "previous_week_total": 0,
            "improvement": 0,
            "type_breakdown": {},
            "best_day": None,
            "total_pushups": 0,
            "daily_average": 0
        }

    # Get current week number
    current_week = pd.Timestamp.now().isocalendar()[1]

    # Add week numbers to dataframe
    df['week'] = df['date'].dt.isocalendar().week

    # Current week stats
    current_week_data = df[df['week'] == current_week]
    previous_week_data = df[df['week'] == (current_week - 1)]

    current_week_total = current_week_data['pushups'].sum()
    previous_week_total = previous_week_data['pushups'].sum()

    # Calculate improvement
    improvement = ((current_week_total - previous_week_total) / previous_week_total * 100) if previous_week_total > 0 else 0

    # Type breakdown for current week
    type_breakdown = current_week_data.groupby('type')['pushups'].agg({
        'total': 'sum',
        'count': 'size',
        'avg': 'mean'
    }).to_dict('index')

    # Best day this week
    best_day = None
    if not current_week_data.empty:
        best_day_series = current_week_data.loc[current_week_data['pushups'].idxmax()]
        best_day = {
            'date': best_day_series['date'],
            'pushups': best_day_series['pushups'],
            'type': best_day_series['type']
        }

    # Daily average for current week
    daily_average = current_week_data['pushups'].mean() if not current_week_data.empty else 0

    return {
        "current_week_total": int(current_week_total),
        "previous_week_total": int(previous_week_total),
        "improvement": round(improvement, 1),
        "type_breakdown": type_breakdown,
        "best_day": best_day,
        "total_pushups": int(current_week_total),
        "daily_average": round(daily_average, 1)
    }