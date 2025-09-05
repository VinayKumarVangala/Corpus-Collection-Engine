import streamlit as st
from .static_categories import get_static_category_id

def get_category_id_from_name(category_name: str) -> str:
    """Map category name to category ID from API"""
    try:
        # Try to get from session state cache first
        if hasattr(st.session_state, 'categories_cache'):
            categories_result = st.session_state.categories_cache
        else:
            categories_result = st.session_state.api_client.get_categories()
            if 'error' not in categories_result and isinstance(categories_result, list):
                st.session_state.categories_cache = categories_result
        
        if 'error' not in categories_result and isinstance(categories_result, list):
            for cat in categories_result:
                if cat.get('title', '').lower() == category_name.lower() or cat.get('name', '').lower() == category_name.lower():
                    return cat.get('id', category_name)
    except Exception as e:
        if hasattr(st, 'error'):
            st.error(f"Category mapping error: {e}")
    
    # Fallback to static mapping, then category name if mapping fails
    static_id = get_static_category_id(category_name)
    return static_id if static_id != category_name else category_name

def get_language_enum(language: str) -> str:
    """Map language to API enum format"""
    language_map = {
        'hindi': 'hindi', 
        'telugu': 'telugu',
        'tamil': 'tamil',
        'kannada': 'kannada',
        'bengali': 'bengali',
        'marathi': 'marathi',
        'gujarati': 'gujarati',
        'malayalam': 'malayalam',
        'punjabi': 'punjabi',
        'assamese': 'assamese',
        'bodo': 'bodo',
        'dogri': 'dogri',
        'kashmiri': 'kashmiri',
        'konkani': 'konkani',
        'maithili': 'maithili',
        'meitei': 'meitei',
        'nepali': 'nepali',
        'odia': 'odia',
        'sanskrit': 'sanskrit',
        'santali': 'santali',
        'sindhi': 'sindhi',
        'urdu': 'urdu'
    }
    
    return language_map.get(language.lower(), 'hindi')  # Default to hindi