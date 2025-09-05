import streamlit as st

def get_category_id_from_name(category_name: str) -> str:
    """Map category name to category ID from API"""
    try:
        categories_result = st.session_state.api_client.get_categories()
        if 'error' not in categories_result and isinstance(categories_result, list):
            for cat in categories_result:
                if cat.get('title', '').lower() == category_name.lower() or cat.get('name', '').lower() == category_name.lower():
                    return cat.get('id', category_name)
    except:
        pass
    
    # Fallback to category name if mapping fails
    return category_name

def get_language_enum(language: str) -> str:
    """Map language to API enum format"""
    language_map = {
        'english': 'english',
        'hindi': 'hindi', 
        'telugu': 'telugu',
        'tamil': 'tamil',
        'kannada': 'kannada',
        'bengali': 'bengali',
        'marathi': 'marathi',
        'gujarati': 'gujarati',
        'malayalam': 'malayalam',
        'punjabi': 'punjabi'
    }
    
    return language_map.get(language.lower(), 'hindi')  # Default to hindi