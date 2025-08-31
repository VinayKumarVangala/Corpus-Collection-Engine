import bcrypt
import jwt
import streamlit as st
from datetime import datetime, timedelta
from config import JWT_SECRET_KEY, BCRYPT_ROUNDS

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=BCRYPT_ROUNDS)).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(user_id: str, email: str) -> str:
    """Create JWT token for user"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    """Get current authenticated user from session"""
    if 'auth_token' in st.session_state:
        payload = verify_jwt_token(st.session_state.auth_token)
        if payload:
            return payload
    return None

def logout():
    """Logout current user"""
    if 'auth_token' in st.session_state:
        del st.session_state.auth_token
    if 'user_id' in st.session_state:
        del st.session_state.user_id
    if 'user_email' in st.session_state:
        del st.session_state.user_email