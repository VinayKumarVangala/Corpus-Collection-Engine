import streamlit as st
import math
from typing import Optional, List, Dict, Any

def get_user_location() -> Optional[Dict[str, float]]:
    """Get user's current location using browser geolocation"""
    # Use Streamlit's built-in location component
    location = st.empty()
    
    # JavaScript to get geolocation
    location_js = """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    }
                }, '*');
            });
        }
    }
    getLocation();
    </script>
    """
    
    return None  # Simplified for now

def search_nearby_records(latitude: float, longitude: float, distance_km: float = 10, 
                         category_id: Optional[str] = None, media_type: Optional[str] = None) -> List[Dict[Any, Any]]:
    """Search for records within specified distance"""
    distance_meters = distance_km * 1000
    
    filters = {}
    if category_id:
        filters['category_id'] = category_id
    if media_type:
        filters['media_type'] = media_type.lower()
    
    result = st.session_state.api_client.search_nearby(latitude, longitude, distance_meters, **filters)
    
    if 'error' not in result:
        return result if isinstance(result, list) else []
    return []

def search_in_bbox(min_lat: float, min_lng: float, max_lat: float, max_lng: float,
                   category_id: Optional[str] = None, media_type: Optional[str] = None) -> List[Dict[Any, Any]]:
    """Search for records within bounding box"""
    filters = {}
    if category_id:
        filters['category_id'] = category_id
    if media_type:
        filters['media_type'] = media_type.lower()
    
    result = st.session_state.api_client.search_bbox(min_lat, min_lng, max_lat, max_lng, **filters)
    
    if 'error' not in result:
        return result if isinstance(result, list) else []
    return []

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in kilometers"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c