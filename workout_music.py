import random
from typing import List, Dict

# Define music categories based on exercise intensity
MUSIC_CATEGORIES = {
    "Low": {
        "bpm_range": (90, 120),
        "description": "Warm-up and light exercises",
        "genres": ["Chill Pop", "Light Rock", "Ambient"],
        "example_songs": [
            "Breathe - Télépopmusik",
            "Yellow - Coldplay",
            "Clocks - Coldplay",
            "Dreams - Fleetwood Mac"
        ]
    },
    "Medium": {
        "bpm_range": (120, 140),
        "description": "Standard pushups and regular exercises",
        "genres": ["Pop", "Rock", "Hip-Hop"],
        "example_songs": [
            "Eye of the Tiger - Survivor",
            "Stronger - Kanye West",
            "Uptown Funk - Mark Ronson ft. Bruno Mars",
            "Can't Hold Us - Macklemore & Ryan Lewis"
        ]
    },
    "High": {
        "bpm_range": (140, 170),
        "description": "Intense exercises like plyometric pushups",
        "genres": ["EDM", "Hard Rock", "High-Energy Pop"],
        "example_songs": [
            "Till I Collapse - Eminem",
            "Stronger - The Score",
            "Remember The Name - Fort Minor",
            "All I Do Is Win - DJ Khaled"
        ]
    },
    "Maximum": {
        "bpm_range": (170, 180),
        "description": "Explosive movements and HIIT",
        "genres": ["Hardcore EDM", "Metal", "Drum and Bass"],
        "example_songs": [
            "Thunderstruck - AC/DC",
            "Survival - Eminem",
            "Push It To The Limit - Paul Engemann",
            "Beast - Rob Bailey & The Hustle Standard"
        ]
    }
}

def get_intensity_for_pushup_type(pushup_type: str) -> str:
    """Determine workout intensity based on pushup type."""
    high_intensity = ["Plyo", "Clap", "One-Handed", "Superman", "Archer"]
    medium_intensity = ["Standard", "Diamond", "Wide Grip", "Close Grip"]
    low_intensity = ["Wall", "Knee", "Incline"]
    
    if pushup_type in high_intensity:
        return "High"
    elif pushup_type in medium_intensity:
        return "Medium"
    elif pushup_type in low_intensity:
        return "Low"
    else:
        return "Medium"

def generate_playlist(intensity: str, duration_minutes: int = 30) -> List[Dict]:
    """Generate a playlist based on workout intensity."""
    if intensity not in MUSIC_CATEGORIES:
        intensity = "Medium"
    
    category = MUSIC_CATEGORIES[intensity]
    songs_needed = duration_minutes // 3  # Assuming average song length of 3 minutes
    
    playlist = []
    available_songs = category["example_songs"].copy()
    
    # Add songs from the intensity category
    while len(playlist) < songs_needed and available_songs:
        song = random.choice(available_songs)
        available_songs.remove(song)
        playlist.append({
            "song": song,
            "genre": random.choice(category["genres"]),
            "bpm": random.randint(category["bpm_range"][0], category["bpm_range"][1])
        })
    
    # If we need more songs, start over with the full list
    while len(playlist) < songs_needed:
        song = random.choice(category["example_songs"])
        playlist.append({
            "song": song,
            "genre": random.choice(category["genres"]),
            "bpm": random.randint(category["bpm_range"][0], category["bpm_range"][1])
        })
    
    return playlist

def get_intensity_description(intensity: str) -> str:
    """Get the description for a given intensity level."""
    return MUSIC_CATEGORIES.get(intensity, MUSIC_CATEGORIES["Medium"])["description"]

def get_recommended_intensity(pushup_count: int) -> str:
    """Get recommended music intensity based on number of pushups."""
    if pushup_count >= 50:
        return "Maximum"
    elif pushup_count >= 30:
        return "High"
    elif pushup_count >= 15:
        return "Medium"
    else:
        return "Low"
