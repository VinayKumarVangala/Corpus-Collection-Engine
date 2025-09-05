import streamlit as st
import hashlib
from datetime import datetime
from pathlib import Path
import json

def handle_offline_login(phone: str, otp: str) -> bool:
    """Handle login in offline mode"""
    if len(otp) == 6:  # Accept any 6-digit OTP
        st.session_state.user_id = hashlib.md5(phone.encode()).hexdigest()[:8]
        st.session_state.user_name = "Demo User"
        st.session_state.user_phone = phone
        return True
    return False

def handle_offline_register(phone: str, name: str, otp: str) -> bool:
    """Handle registration in offline mode"""
    if len(otp) == 6:  # Accept any 6-digit OTP
        # Save user locally
        st.session_state.registered_users[phone] = {
            'name': name,
            'created_at': datetime.now().isoformat()
        }
        
        # Save to file
        Path("data").mkdir(exist_ok=True)
        with open("data/users.json", 'w') as f:
            json.dump(st.session_state.registered_users, f, indent=2)
        
        st.session_state.user_id = hashlib.md5(phone.encode()).hexdigest()[:8]
        st.session_state.user_name = name
        st.session_state.user_phone = phone
        return True
    return False

def save_offline_contribution(contribution_data: dict, content_data) -> bool:
    """Save contribution in offline mode"""
    contribution = {
        "id": hashlib.md5(f"{st.session_state.user_id}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
        "user_id": st.session_state.user_id,
        "category": contribution_data["category"],
        "media_type": contribution_data["media_type"],
        "title": contribution_data["title"],
        "description": contribution_data.get("description", ""),
        "language": contribution_data["language"],
        "public": contribution_data.get("public", False),
        "timestamp": datetime.now().isoformat(),
        "size": len(str(content_data)) if contribution_data["media_type"] == "Text" else len(content_data.getvalue()) if hasattr(content_data, 'getvalue') else 0
    }
    
    # Add to session state
    st.session_state.contributions.append(contribution)
    
    # Save to file
    Path("data").mkdir(exist_ok=True)
    with open("data/contributions.json", 'w') as f:
        json.dump(st.session_state.contributions, f, indent=2)
    
    # Save content file
    if contribution["media_type"] == "Text":
        content_file = Path("data") / f"{contribution['id']}.txt"
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(str(content_data))
    else:
        uploads_dir = Path("data/uploads")
        uploads_dir.mkdir(exist_ok=True)
        file_extension = content_data.name.split('.')[-1] if '.' in content_data.name else 'bin'
        content_file = uploads_dir / f"{contribution['id']}.{file_extension}"
        with open(content_file, 'wb') as f:
            content_data.seek(0)
            f.write(content_data.read())
    
    return True