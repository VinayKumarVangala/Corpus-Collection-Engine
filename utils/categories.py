import streamlit as st
from typing import Dict, List

def get_categories() -> Dict[str, str]:
    """Get categories from API or fallback to local"""
    try:
        result = st.session_state.api_client.get_categories()
        if 'error' not in result and isinstance(result, list):
            # Convert API response to emoji dict
            categories = {}
            emoji_map = {
                "art": "🎨", "meme": "😂", "culture": "🏛️", "food": "🍛",
                "fables": "📚", "events": "🎉", "music": "🎵", "people": "👥",
                "literature": "📖", "architecture": "🏗️", "skills": "⚡",
                "images": "📸", "videos": "🎬", "flora": "🌸", "fauna": "🦋",
                "education": "🎓", "vegetation": "🌿", "folk talks": "🗣️",
                "traditional skills": "🛠️", "local history": "📜",
                "local locations": "📍", "food & agriculture": "🌾",
                "newspapers": "📰"
            }
            
            for cat in result:
                name = cat.get('name', '').lower()
                title = cat.get('title', cat.get('name', ''))
                emoji = emoji_map.get(name, "📝")
                categories[title] = emoji
            
            return categories
    except:
        pass
    
    # Fallback to local categories
    return {
        "Art": "🎨", "Meme": "😂", "Culture": "🏛️", "Food": "🍛",
        "Fables": "📚", "Events": "🎉", "Music": "🎵", "People": "👥",
        "Literature": "📖", "Architecture": "🏗️", "Skills": "⚡",
        "Images": "📸", "Videos": "🎬", "Flora": "🌸", "Fauna": "🦋",
        "Education": "🎓", "Vegetation": "🌿", "Folk Talks": "🗣️",
        "Traditional Skills": "🛠️", "Local History": "📜",
        "Local Locations": "📍", "Food & Agriculture": "🌾",
        "Newspapers": "📰"
    }