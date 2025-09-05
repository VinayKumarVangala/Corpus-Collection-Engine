import requests
import json
from typing import Optional, Dict, Any
from pathlib import Path
import streamlit as st
from config import API_TIMEOUT, DEBUG

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = self._load_token()
        if self.token:
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
    
    def _load_token(self) -> Optional[str]:
        """Load JWT token from storage"""
        token_file = Path("data/token.json")
        if token_file.exists():
            try:
                with open(token_file, 'r') as f:
                    data = json.load(f)
                return data.get('access_token')
            except:
                return None
        return None
    
    def _save_token(self, token: str):
        """Save JWT token to storage"""
        Path("data").mkdir(exist_ok=True)
        with open("data/token.json", 'w') as f:
            json.dump({'access_token': token}, f)
        self.token = token
        self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    def _clear_token(self):
        """Clear stored token"""
        token_file = Path("data/token.json")
        if token_file.exists():
            token_file.unlink()
        self.token = None
        self.session.headers.pop('Authorization', None)
    
    def request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make API request with error handling"""
        url = f"{self.base_url}/api/v1{endpoint}"
        
        # Set timeout if not provided
        if 'timeout' not in kwargs:
            kwargs['timeout'] = API_TIMEOUT
            
        try:
            if DEBUG:
                st.write(f"API Request: {method} {url}")
                
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            # Handle different response types
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                return response.json()
            else:
                return {"message": "Success", "status_code": response.status_code}
                
        except requests.exceptions.RequestException as e:
            error_msg = f"API Connection Error: {str(e)}"
            if DEBUG:
                st.error(error_msg)
            else:
                st.error("Unable to connect to server. Please check your internet connection.")
            return {"error": str(e)}
    
    # Authentication endpoints
    def send_signup_otp(self, phone: str) -> Dict[Any, Any]:
        return self.request('POST', '/auth/signup/send-otp', json={'phone': phone})
    
    def verify_signup_otp(self, phone: str, otp: str, name: str) -> Dict[Any, Any]:
        data = {'phone': phone, 'otp': otp, 'name': name}
        result = self.request('POST', '/auth/signup/verify-otp', json=data)
        if 'access_token' in result:
            self._save_token(result['access_token'])
        return result
    
    def send_login_otp(self, phone: str) -> Dict[Any, Any]:
        return self.request('POST', '/auth/login/send-otp', json={'phone': phone})
    
    def verify_login_otp(self, phone: str, otp: str) -> Dict[Any, Any]:
        data = {'phone': phone, 'otp': otp}
        result = self.request('POST', '/auth/login/verify-otp', json=data)
        if 'access_token' in result:
            self._save_token(result['access_token'])
        return result
    
    def get_current_user(self) -> Dict[Any, Any]:
        return self.request('GET', '/auth/me')
    
    def export_user_data(self, export_format: str = 'json') -> Dict[Any, Any]:
        return self.request('POST', '/tasks/export-data', params={'export_format': export_format})
    
    def logout(self):
        self._clear_token()
    
    # Geospatial endpoints
    def search_nearby(self, latitude: float, longitude: float, distance_meters: float, **filters) -> Dict[Any, Any]:
        params = {
            'latitude': latitude,
            'longitude': longitude, 
            'distance_meters': distance_meters,
            **filters
        }
        return self.request('GET', '/records/search/nearby', params=params)
    
    def search_bbox(self, min_lat: float, min_lng: float, max_lat: float, max_lng: float, **filters) -> Dict[Any, Any]:
        params = {
            'min_lat': min_lat,
            'min_lng': min_lng,
            'max_lat': max_lat,
            'max_lng': max_lng,
            **filters
        }
        return self.request('GET', '/records/search/bbox', params=params)
    
    # Categories
    def get_categories(self) -> Dict[Any, Any]:
        return self.request('GET', '/categories/')
    
    # Records
    def create_record(self, record_data: Dict[Any, Any]) -> Dict[Any, Any]:
        return self.request('POST', '/records/', json=record_data)
    
    def get_user_contributions(self, user_id: str) -> Dict[Any, Any]:
        return self.request('GET', f'/users/{user_id}/contributions')
    
    def get_records(self, **filters) -> Dict[Any, Any]:
        return self.request('GET', '/records/', params=filters)
    
    # Admin endpoints
    def get_all_users(self, skip: int = 0, limit: int = 100) -> Dict[Any, Any]:
        return self.request('GET', '/users/', params={'skip': skip, 'limit': limit})
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[Any, Any]:
        return self.request('POST', '/categories/', json=category_data)
    
    def delete_category(self, category_id: str) -> Dict[Any, Any]:
        return self.request('DELETE', f'/categories/{category_id}')
    
    def get_user_roles(self, user_id: str) -> Dict[Any, Any]:
        return self.request('GET', f'/users/{user_id}/roles')
    
    def assign_role_to_user(self, user_id: str, role_id: int) -> Dict[Any, Any]:
        return self.request('PUT', f'/users/{user_id}/roles/add', params={'role_id': role_id})
    
    def health_check(self) -> Dict[Any, Any]:
        return self.request('GET', '/health')