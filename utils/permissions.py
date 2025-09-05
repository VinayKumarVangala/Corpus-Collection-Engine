import streamlit as st
from typing import List, Dict, Any

def get_user_roles() -> List[Dict[str, Any]]:
    """Get current user's roles"""
    if not st.session_state.user_id:
        return []
    
    result = st.session_state.api_client.request('GET', f'/users/{st.session_state.user_id}/roles')
    
    if 'error' not in result and isinstance(result, list):
        return result
    return []

def has_permission(permission: str) -> bool:
    """Check if user has specific permission"""
    roles = get_user_roles()
    
    # Admin permissions
    admin_permissions = [
        'users:read', 'users:write', 'users:delete',
        'records:read', 'records:write', 'records:delete',
        'categories:read', 'categories:write', 'categories:delete'
    ]
    
    # Reviewer permissions
    reviewer_permissions = [
        'users:read', 'records:read', 'records:write'
    ]
    
    for role in roles:
        role_name = role.get('name', '').lower()
        
        if role_name == 'admin' and permission in admin_permissions:
            return True
        elif role_name == 'reviewer' and permission in reviewer_permissions:
            return True
        elif role_name == 'user' and permission in ['records:read']:
            return True
    
    return False

def is_admin() -> bool:
    """Check if user is admin"""
    return has_permission('users:write')

def is_reviewer() -> bool:
    """Check if user is reviewer"""
    return has_permission('records:write') and not is_admin()

def can_export_data() -> bool:
    """Check if user can export data"""
    return is_admin() or is_reviewer()

def get_user_with_roles(user_id: str) -> Dict[str, Any]:
    """Get user info with roles"""
    result = st.session_state.api_client.request('GET', f'/users/{user_id}/with-roles')
    
    if 'error' not in result:
        return result
    return {}