import streamlit as st
import json
import hashlib
from datetime import datetime
from pathlib import Path
import os
import bcrypt
from config import API_BASE_URL, ENVIRONMENT, DEBUG
from utils.api_client import APIClient
from utils.categories import get_categories
from utils.file_upload import upload_file_chunked, validate_file_size
from utils.category_mapper import get_category_id_from_name, get_language_enum
from utils.geospatial import search_nearby_records, search_in_bbox
from utils.permissions import has_permission, is_admin, can_export_data
from utils.data_export import export_user_data, format_export_data
from admin_panel import show_admin_panel

# Page config
st.set_page_config(
    page_title="Corpus Collection Engine",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Color Scheme CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #2c3e50;
    }
    

    
    /* Card-style category buttons */
    .category-card {
        background: white;
        border-radius: 16px;
        padding: 24px 16px;
        margin: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        cursor: pointer;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .category-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border-color: #3498db;
    }
    
    .category-icon {
        font-size: 48px;
        margin-bottom: 12px;
        display: block;
    }
    
    .category-title {
        font-size: 18px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 8px;
    }
    
    .category-description {
        font-size: 12px;
        color: #6c757d;
        line-height: 1.4;
        text-align: center;
    }

    
    /* Category buttons - square styling */
    .category-button-container .stButton > button {
        width: 100% !important;
        height: 180px !important;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        font-size: 14px !important;
        color: #2c3e50 !important;
        margin-bottom: 15px !important;
        white-space: pre-line !important;
        padding: 20px !important;
    }
    
    .category-button-container .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
        border-color: #007bff !important;
        background: linear-gradient(135deg, #e9ecef 0%, #f8f9fa 100%) !important;
    }
    
    /* Regular buttons - normal styling */
    .stButton > button:not(.category-button-container .stButton > button) {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
    }
    
    .stButton > button:not(.category-button-container .stButton > button):hover {
        background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
    }
    
    .header-container {
        background: linear-gradient(135deg, #d35400 0%, #e67e22 100%);
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 40px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(44, 62, 80, 0.3);
    }
    
    .stSelectbox > div > div {
        background: white;
        border-radius: 12px;
        border: 2px solid #e9ecef;
    }
    
    .stTextInput > div > div > input {
        background: white;
        border-radius: 12px;
        border: 2px solid #e9ecef;
    }
    
    .stTextArea > div > div > textarea {
        background: white;
        border-radius: 12px;
        border: 2px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# API-compatible categories (fallback if API unavailable)
CATEGORIES = {
    "Art": "🎨",
    "Culture": "🏛️",
    "Food": "🍛",
    "Literature": "📖",
    "Music": "🎵",
    "Architecture": "🏗️",
    "Education": "🎓",
    "Flora": "🌸",
    "Fauna": "🦋",
    "Events": "🎉"
}

MEDIA_TYPES = ["Text", "Image", "Audio", "Video"]

# Dynamic categories from API
def get_current_categories():
    """Get categories with caching"""
    if 'categories' not in st.session_state:
        st.session_state.categories = get_categories()
    return st.session_state.categories

# Local storage functions for offline mode
def load_users():
    users_file = Path("data/users.json")
    if users_file.exists():
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    Path("data").mkdir(exist_ok=True)
    with open("data/users.json", 'w') as f:
        json.dump(users, f, indent=2)

def load_contributions():
    contrib_file = Path("data/contributions.json")
    if contrib_file.exists():
        with open(contrib_file, 'r') as f:
            return json.load(f)
    return []

def save_contributions(contributions):
    Path("data").mkdir(exist_ok=True)
    with open("data/contributions.json", 'w') as f:
        json.dump(contributions, f, indent=2)

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def restore_user_session():
    """Restore user session from persistent storage if available"""
    session_file = Path("data/current_session.json")
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            if session_data.get('user_id'):
                st.session_state.user_id = session_data['user_id']
                st.session_state.user_phone = session_data.get('user_phone')
                st.session_state.user_name = session_data.get('user_name')
                st.session_state.page = session_data.get('page', 'Home')
        except:
            pass

def save_user_session():
    """Save current user session to persistent storage"""
    if st.session_state.user_id:
        session_data = {
            'user_id': st.session_state.user_id,
            'user_phone': st.session_state.user_phone,
            'user_name': st.session_state.user_name,
            'page': st.session_state.page
        }
        Path("data").mkdir(exist_ok=True)
        with open("data/current_session.json", 'w') as f:
            json.dump(session_data, f, indent=2)

def clear_user_session():
    """Clear saved user session"""
    session_file = Path("data/current_session.json")
    if session_file.exists():
        session_file.unlink()

def format_file_size(size_bytes):
    """Format file size with appropriate unit (B, KB, MB, GB, TB)"""
    if size_bytes == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"

# Initialize API client
if 'api_client' not in st.session_state:
    st.session_state.api_client = APIClient(API_BASE_URL)

# Initialize session state with persistent data
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_phone' not in st.session_state:
    st.session_state.user_phone = None
if 'contributions' not in st.session_state:
    st.session_state.contributions = load_contributions()
if 'offline_queue' not in st.session_state:
    st.session_state.offline_queue = []
if 'registered_users' not in st.session_state:
    st.session_state.registered_users = load_users()
if 'page_history' not in st.session_state:
    st.session_state.page_history = []
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'pending_phone' not in st.session_state:
    st.session_state.pending_phone = None

# Restore user session on app restart
restore_user_session()

if 'page' not in st.session_state:
    st.session_state.page = "Login" if not st.session_state.user_id else "Home"

def main():
    # Header with modern styling
    st.markdown("""
    <div class="header-container">
        <h1>🔗 Corpus Collection Engine</h1>
        <p style="font-size: 18px; margin-top: 10px;">Preserving Indian Culture & Diversity</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create top navbar
    if st.session_state.user_id:
        nav_options = ["Home", "Contribute", "Dashboard", "Browse", "About"]
        
        # Add Admin option for admin users
        if is_admin():
            nav_options.append("Admin")
            nav_cols = st.columns([1, 1, 1, 1, 1, 1, 0.5])
        else:
            nav_cols = st.columns([1, 1, 1, 1, 1, 0.5])
        
        for i, option in enumerate(nav_options):
            with nav_cols[i]:
                button_type = "primary" if option == st.session_state.page else "secondary"
                if option == "Admin":
                    button_type = "secondary"  # Admin button always secondary style
                    
                if st.button(option, key=f"nav_{option}", use_container_width=True, type=button_type):
                    if st.session_state.page != option:
                        st.session_state.page = option
                        save_user_session()
                        st.rerun()
        
        # Logout button with role indicator
        logout_col_index = len(nav_options)
        with nav_cols[logout_col_index]:
            # Show user role if admin/reviewer
            if is_admin():
                st.caption("🔑 Admin")
            elif has_permission('records:write'):
                st.caption("🔍 Reviewer")
                
            if st.button("Logout", key="logout_btn", use_container_width=True, type="secondary"):
                # Clear API session and local session
                st.session_state.api_client.logout()
                clear_user_session()
                st.session_state.user_id = None
                st.session_state.user_name = None
                st.session_state.user_phone = None
                st.session_state.otp_sent = False
                st.session_state.pending_phone = None
                st.session_state.page = "Login"
                st.rerun()
    else:
        nav_options = ["Login", "Home", "About"]
        nav_cols = st.columns(len(nav_options))
        for i, option in enumerate(nav_options):
            with nav_cols[i]:
                if st.button(option, key=f"nav_{option}", use_container_width=True,
                           type="primary" if option == st.session_state.page else "secondary"):
                    if st.session_state.page != option:
                        st.session_state.page = option
                        st.rerun()
    
    page = st.session_state.page
    
    st.divider()
    
    # Route to pages
    if page == "Home":
        show_home()
    elif page == "Login":
        show_login()
    elif page == "Contribute":
        show_contribute()
    elif page == "Dashboard":
        show_dashboard()
    elif page == "Browse":
        show_browse()
    elif page == "About":
        show_about()
    elif page == "Admin":
        show_admin_panel()

def show_home():
    if st.session_state.user_id:
        # Welcome message for logged-in users using their name
        username = st.session_state.get('user_name', 'User')
        st.header(f"Welcome {username}!! 🎉")
    else:
        st.header("Welcome to the Corpus Collection Engine")
        st.info("Please login to start contributing to preserve Indian cultural heritage!")
        return
    
    st.markdown("<h2 style='color: #2c3e50; margin-bottom: 30px; text-align: center;'>🎯 Choose a Category to Contribute</h2>", unsafe_allow_html=True)
    
    # Custom CSS for square category buttons
    st.markdown("""
    <style>
    .category-button {
        width: 100% !important;
        height: 180px !important;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        font-size: 14px !important;
        color: #2c3e50 !important;
        margin-bottom: 15px !important;
        white-space: pre-line !important;
    }
    .category-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
        border-color: #007bff !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Category descriptions
    descriptions = {
        "Art": "Creative works, paintings, sculptures, and artistic expressions",
        "Culture": "Traditions, customs, folklore, memes, people, and cultural practices",
        "Food": "Culinary content, recipes, agriculture, and food-related information",
        "Literature": "Books, poems, stories, fables, newspapers, and written works",
        "Music": "Musical content, songs, instruments, and audio experiences",
        "Architecture": "Buildings, structures, monuments, and architectural designs",
        "Education": "Learning materials, skills, tutorials, and educational content",
        "Flora": "Plants, flowers, trees, vegetation, and botanical content",
        "Fauna": "Animals, wildlife, birds, and zoological content",
        "Events": "Festivals, celebrations, ceremonies, and special occasions"
    }
    
    # Category grid - 4 columns per row
    cols_per_row = 4
    categories = get_current_categories()
    categories_list = list(categories.items())
    
    for i in range(0, len(categories_list), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, col in enumerate(cols):
            if i + j < len(categories_list):
                category, emoji = categories_list[i + j]
                
                with col:
                    # Direct functional button with custom styling
                    button_content = f"{emoji}\n\n**{category}**\n\n{descriptions.get(category, 'Cultural content and information')}"
                    
                    # Apply custom CSS class to button
                    st.markdown('<div class="category-button-container">', unsafe_allow_html=True)
                    if st.button(button_content, key=f"cat_{i+j}", help=f"Contribute to {category}", use_container_width=True):
                        st.session_state.selected_category = category
                        st.session_state.page = "Contribute"
                        save_user_session()
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

def show_login():
    st.header("Login / Register")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login with Phone")
        phone = st.text_input("Phone Number", placeholder="+91XXXXXXXXXX")
        
        if not st.session_state.otp_sent:
            if st.button("Send OTP", type="primary"):
                if phone:
                    result = st.session_state.api_client.send_login_otp(phone)
                    if 'error' not in result:
                        st.session_state.otp_sent = True
                        st.session_state.pending_phone = phone
                        st.success("OTP sent to your phone!")
                        st.rerun()
                    else:
                        st.error("Failed to send OTP. Please try again.")
                else:
                    st.error("Please enter your phone number.")
        else:
            otp = st.text_input("Enter OTP", max_chars=6)
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Verify OTP", type="primary"):
                    if otp:
                        result = st.session_state.api_client.verify_login_otp(st.session_state.pending_phone, otp)
                        if 'access_token' in result:
                            # Get user info
                            user_info = st.session_state.api_client.get_current_user()
                            if 'error' not in user_info:
                                st.session_state.user_id = user_info['id']
                                st.session_state.user_name = user_info.get('name', 'User')
                                st.session_state.user_phone = st.session_state.pending_phone
                                st.session_state.page = "Home"
                                st.session_state.otp_sent = False
                                st.session_state.pending_phone = None
                                st.success("Logged in successfully!")
                                st.balloons()
                                st.rerun()
                        else:
                            st.error("Invalid OTP. Please try again.")
                    else:
                        st.error("Please enter the OTP.")
            
            with col2:
                if st.button("Resend OTP"):
                    result = st.session_state.api_client.send_login_otp(st.session_state.pending_phone)
                    if 'error' not in result:
                        st.success("OTP resent!")
                    else:
                        st.error("Failed to resend OTP.")
    
    with tab2:
        st.subheader("Register with Phone")
        reg_phone = st.text_input("Phone Number", key="reg_phone", placeholder="+91XXXXXXXXXX")
        reg_name = st.text_input("Display Name")
        
        if not st.session_state.otp_sent:
            if st.button("Send OTP", key="reg_send_otp", type="primary"):
                if reg_phone and reg_name:
                    result = st.session_state.api_client.send_signup_otp(reg_phone)
                    if 'error' not in result:
                        st.session_state.otp_sent = True
                        st.session_state.pending_phone = reg_phone
                        st.session_state.pending_name = reg_name
                        st.success("OTP sent to your phone!")
                        st.rerun()
                    else:
                        st.error("Failed to send OTP. Please try again.")
                else:
                    st.error("Please fill in all fields.")
        else:
            otp = st.text_input("Enter OTP", key="reg_otp", max_chars=6)
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Verify & Register", type="primary"):
                    if otp:
                        result = st.session_state.api_client.verify_signup_otp(
                            st.session_state.pending_phone, 
                            otp, 
                            st.session_state.pending_name
                        )
                        if 'access_token' in result:
                            # Get user info
                            user_info = st.session_state.api_client.get_current_user()
                            if 'error' not in user_info:
                                st.session_state.user_id = user_info['id']
                                st.session_state.user_name = user_info.get('name', 'User')
                                st.session_state.user_phone = st.session_state.pending_phone
                                st.session_state.page = "Home"
                                st.session_state.otp_sent = False
                                st.session_state.pending_phone = None
                                st.success("Registered successfully!")
                                st.balloons()
                                st.rerun()
                        else:
                            st.error("Registration failed. Please try again.")
                    else:
                        st.error("Please enter the OTP.")
            
            with col2:
                if st.button("Resend OTP", key="reg_resend"):
                    result = st.session_state.api_client.send_signup_otp(st.session_state.pending_phone)
                    if 'error' not in result:
                        st.success("OTP resent!")
                    else:
                        st.error("Failed to resend OTP.")

def show_contribute():
    if not st.session_state.user_id:
        st.warning("Please login first!")
        return
    
    st.header("Contribute Content")
    
    # Step 1: Category Selection
    categories = get_current_categories()
    if 'selected_category' in st.session_state and st.session_state.selected_category:
        category = st.selectbox("Select Category", list(categories.keys()), 
                               index=list(categories.keys()).index(st.session_state.selected_category))
    else:
        category = st.selectbox("Select Category", list(categories.keys()))
    
    # Step 2: Media Type
    media_type = st.selectbox("Select Media Type", MEDIA_TYPES)
    
    # Step 3: Content Input
    st.subheader(f"Add {media_type} Content")
    
    content_data = None
    metadata = {}
    
    if media_type == "Text":
        content_data = st.text_area("Enter your text content", height=200)
        
    elif media_type == "Image":
        uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            content_data = uploaded_file
            st.image(uploaded_file, caption="Preview", width=300)
            
    elif media_type == "Audio":
        uploaded_file = st.file_uploader("Upload Audio", type=['mp3', 'wav', 'ogg'])
        if uploaded_file:
            content_data = uploaded_file
            st.audio(uploaded_file)
            
    elif media_type == "Video":
        uploaded_file = st.file_uploader("Upload Video", type=['mp4', 'avi', 'mov'])
        if uploaded_file:
            content_data = uploaded_file
            st.video(uploaded_file)
    
    # Step 4: Metadata
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Title (optional)")
        language = st.selectbox("Language", ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Bengali", "Marathi", "Gujarati", "Malayalam", "Punjabi"])
    
    with col2:
        description = st.text_area("Description (optional)", height=100)
        public_consent = st.checkbox("Make this contribution public")
    
    # Step 4.5: Location (optional)
    st.subheader("🗺️ Location (Optional)")
    add_location = st.checkbox("Add location to this contribution")
    
    latitude = None
    longitude = None
    
    if add_location:
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Latitude", value=17.385, format="%.6f", help="Decimal degrees")
        with col2:
            longitude = st.number_input("Longitude", value=78.4867, format="%.6f", help="Decimal degrees")
        
        st.info("📍 This will help others discover your contribution based on location.")
    
    # Step 5: Submit
    if st.button("Submit Contribution", type="primary"):
        if content_data:
            # Validate file size for non-text content
            if media_type != "Text" and not validate_file_size(content_data, media_type):
                return
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                if media_type == "Text":
                    # For text, create record directly
                    api_record = {
                        "title": title or f"{media_type} contribution",
                        "description": description,
                        "category_id": get_category_id_from_name(category),
                        "media_type": media_type.lower(),
                        "content": str(content_data),
                        "language": get_language_enum(language),
                        "release_rights": "public" if public_consent else "private"
                    }
                    
                    progress_bar.progress(50)
                    status_text.text("Creating text record...")
                    
                    result = st.session_state.api_client.create_record(api_record)
                    
                    if 'error' not in result:
                        progress_bar.progress(100)
                        status_text.text("Success!")
                        st.success("Text contribution submitted successfully!")
                        st.balloons()
                        
                        # Clear form
                        if 'selected_category' in st.session_state:
                            del st.session_state.selected_category
                    else:
                        st.error(f"Failed to submit: {result['error']}")
                        
                else:
                    # For files, use chunked upload
                    status_text.text("Uploading file...")
                    progress_bar.progress(25)
                    
                    record_data = {
                        "title": title or f"{media_type} contribution",
                        "description": description,
                        "category_id": get_category_id_from_name(category),
                        "media_type": media_type,
                        "language": get_language_enum(language),
                        "public": public_consent,
                        "latitude": latitude,
                        "longitude": longitude
                    }
                    
                    record_id = upload_file_chunked(content_data, record_data)
                    
                    if record_id:
                        progress_bar.progress(100)
                        status_text.text("Success!")
                        st.success("File contribution submitted successfully!")
                        st.balloons()
                        
                        # Clear form
                        if 'selected_category' in st.session_state:
                            del st.session_state.selected_category
                    else:
                        st.error("Failed to upload file. Please try again.")
                        
            except Exception as e:
                st.error(f"Submission error: {str(e)}")
            finally:
                progress_bar.empty()
                status_text.empty()
                
        else:
            st.error("Please provide content before submitting!")

def show_dashboard():
    if not st.session_state.user_id:
        st.warning("Please login first!")
        return
    
    st.header("Your Dashboard")
    
    # Fetch user contributions from API
    with st.spinner("Loading your contributions..."):
        contributions_data = st.session_state.api_client.get_user_contributions(st.session_state.user_id)
    
    if 'error' in contributions_data:
        st.error("Failed to load contributions. Please try again.")
        return
    
    total_contributions = contributions_data.get('total_contributions', 0)
    
    if total_contributions == 0:
        st.info("No contributions yet. Start contributing to see your stats!")
        return
    
    # Stats with colorful cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Get media type counts
    media_counts = contributions_data.get('contributions_by_media_type', {})
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 6px 20px rgba(52, 152, 219, 0.3); border: 1px solid #e9ecef;">
            <h3 style="color: white; margin: 0; font-size: 28px;">📊</h3>
            <h2 style="color: white; margin: 10px 0; font-size: 32px;">{total_contributions}</h2>
            <p style="color: white; margin: 0; font-size: 14px;">Total Contributions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Calculate total duration for audio/video
        audio_duration = contributions_data.get('audio_duration', 0)
        video_duration = contributions_data.get('video_duration', 0)
        total_duration = audio_duration + video_duration
        duration_text = f"{total_duration//60}m {total_duration%60}s" if total_duration > 0 else "0s"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 6px 20px rgba(46, 204, 113, 0.3); border: 1px solid #e9ecef;">
            <h3 style="color: white; margin: 0; font-size: 28px;">⏱️</h3>
            <h2 style="color: white; margin: 10px 0; font-size: 32px;">{duration_text}</h2>
            <p style="color: white; margin: 0; font-size: 14px;">Media Duration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Count unique categories from contributions
        all_contributions = []
        for media_type in ['text_contributions', 'audio_contributions', 'video_contributions', 'image_contributions', 'document_contributions']:
            contribs = contributions_data.get(media_type, [])
            if contribs:
                all_contributions.extend(contribs)
        
        unique_categories = len(set(c.get('category_id', '') for c in all_contributions if c.get('category_id')))
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 6px 20px rgba(231, 76, 60, 0.3); border: 1px solid #e9ecef;">
            <h3 style="color: white; margin: 0; font-size: 28px;">📂</h3>
            <h2 style="color: white; margin: 10px 0; font-size: 32px;">{unique_categories}</h2>
            <p style="color: white; margin: 0; font-size: 14px;">Categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Count public contributions
        public_count = sum(1 for c in all_contributions if c.get('release_rights') == 'public')
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 6px 20px rgba(243, 156, 18, 0.3); border: 1px solid #e9ecef;">
            <h3 style="color: white; margin: 0; font-size: 28px;">🌍</h3>
            <h2 style="color: white; margin: 10px 0; font-size: 32px;">{public_count}</h2>
            <p style="color: white; margin: 0; font-size: 14px;">Public Contributions</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Media type breakdown
    st.subheader("Contributions by Media Type")
    if media_counts:
        chart_data = {
            'Text': media_counts.get('text', 0),
            'Audio': media_counts.get('audio', 0),
            'Video': media_counts.get('video', 0),
            'Image': media_counts.get('image', 0),
            'Document': media_counts.get('document', 0)
        }
        # Filter out zero values
        chart_data = {k: v for k, v in chart_data.items() if v > 0}
        if chart_data:
            st.bar_chart(chart_data)
    
    # Data Export Section
    if can_export_data():
        st.subheader("📥 Data Export")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            export_format = st.selectbox("Export Format", ["JSON", "CSV"])
        
        with col2:
            if st.button("Export My Data", type="secondary"):
                with st.spinner("Preparing export..."):
                    export_result = export_user_data(export_format.lower())
                    
                    if 'error' not in export_result:
                        st.success("Export initiated! Check back in a few minutes.")
                        if 'task_id' in export_result:
                            st.info(f"Task ID: {export_result['task_id']}")
                    else:
                        st.error(f"Export failed: {export_result['error']}")
        
        with col3:
            st.info("🔒 Available for authorized users")
    
    # Recent contributions
    st.subheader("Recent Contributions")
    recent_contributions = all_contributions[:5] if all_contributions else []
    
    for contrib in recent_contributions:
        with st.expander(f"{contrib.get('title', 'Untitled')} ({contrib.get('media_type', 'Unknown').title()})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Category ID:** {contrib.get('category_id', 'N/A')}")
                st.write(f"**Language:** {contrib.get('language', 'N/A').title()}")
                # Show location if available
                if contrib.get('latitude') and contrib.get('longitude'):
                    st.write(f"🗺️ **Location:** {contrib['latitude']:.4f}, {contrib['longitude']:.4f}")
            with col2:
                timestamp = contrib.get('timestamp')
                if timestamp:
                    date_str = timestamp[:10] if len(timestamp) >= 10 else timestamp
                    st.write(f"**Date:** {date_str}")
                st.write(f"**Public:** {'Yes' if contrib.get('release_rights') == 'public' else 'No'}")
                if contrib.get('size'):
                    st.write(f"**Size:** {format_file_size(contrib['size'])}")

def show_browse():
    st.header("Browse Public Contributions")
    
    # Search mode selection
    search_mode = st.radio("Search Mode", ["All Records", "Location-based Search"], horizontal=True)
    
    if search_mode == "Location-based Search":
        st.subheader("🗺️ Location-based Search")
        
        # Location input
        col1, col2, col3 = st.columns(3)
        with col1:
            latitude = st.number_input("Latitude", value=17.385, format="%.6f")
        with col2:
            longitude = st.number_input("Longitude", value=78.4867, format="%.6f")
        with col3:
            distance = st.slider("Search Radius (km)", 1, 50, 10)
        
        # Additional filters
        col1, col2 = st.columns(2)
        with col1:
            categories = get_current_categories()
            filter_category = st.selectbox("Filter by Category", ["All"] + list(categories.keys()))
        with col2:
            filter_media = st.selectbox("Filter by Media Type", ["All"] + ["Text", "Audio", "Video", "Image", "Document"])
        
        if st.button("Search Nearby", type="primary"):
            with st.spinner("Searching nearby contributions..."):
                category_id = None if filter_category == "All" else get_category_id_from_name(filter_category)
                media_type = None if filter_media == "All" else filter_media
                
                nearby_records = search_nearby_records(latitude, longitude, distance, category_id, media_type)
                
                if nearby_records:
                    st.success(f"Found {len(nearby_records)} contributions within {distance}km")
                    
                    for record in nearby_records:
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**{record.get('title', 'Untitled')}**")
                                media_type_display = record.get('media_type', 'unknown').title()
                                language_display = record.get('language', 'unknown').title()
                                st.write(f"Type: {media_type_display} | Language: {language_display}")
                                if record.get('description'):
                                    st.write(record['description'])
                            with col2:
                                # Show distance if available
                                if 'distance' in record:
                                    st.write(f"📍 {record['distance']:.1f}km")
                                timestamp = record.get('created_at') or record.get('timestamp')
                                if timestamp:
                                    date_str = timestamp[:10] if len(timestamp) >= 10 else timestamp
                                    st.write(f"📅 {date_str}")
                            st.divider()
                else:
                    st.info("No contributions found in this area.")
        return
    
    # Regular filters for "All Records" mode
    col1, col2, col3 = st.columns(3)
    
    # Get categories for filter
    categories = get_current_categories()
    
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(categories.keys()))
    with col2:
        filter_media = st.selectbox("Filter by Media Type", ["All"] + ["Text", "Audio", "Video", "Image", "Document"])
    with col3:
        filter_language = st.selectbox("Filter by Language", ["All", "English", "Hindi", "Telugu", "Tamil", "Kannada"])
    
    # Fetch public records from API
    with st.spinner("Loading public contributions..."):
        filters = {}
        if filter_category != "All":
            filters['category_id'] = filter_category
        if filter_media != "All":
            filters['media_type'] = filter_media.lower()
        
        records = st.session_state.api_client.get_records(**filters)
    
    if 'error' in records:
        st.error("Failed to load contributions. Please try again.")
        return
    
    # Filter by language if specified
    if filter_language != "All":
        records = [r for r in records if r.get('language', '').lower() == filter_language.lower()]
    
    # Only show public records
    public_records = [r for r in records if r.get('release_rights') == 'public']
    
    st.write(f"Found {len(public_records)} public contributions")
    
    # Display contributions
    for record in public_records:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{record.get('title', 'Untitled')}**")
                media_type = record.get('media_type', 'unknown').title()
                language = record.get('language', 'unknown').title()
                category_id = record.get('category_id', 'N/A')
                st.write(f"Category: {category_id} | Type: {media_type} | Language: {language}")
                if record.get('description'):
                    st.write(record['description'])
                
                # Show location if available
                if record.get('latitude') and record.get('longitude'):
                    st.write(f"📍 Location: {record['latitude']:.4f}, {record['longitude']:.4f}")
                    
            with col2:
                timestamp = record.get('created_at') or record.get('timestamp')
                if timestamp:
                    date_str = timestamp[:10] if len(timestamp) >= 10 else timestamp
                    st.write(f"📅 {date_str}")
                if record.get('size'):
                    st.write(f"📊 {format_file_size(record['size'])}")
                    
                # Admin actions
                if is_admin():
                    if st.button(f"View Details", key=f"view_{record.get('id')}", help="Admin view"):
                        st.info(f"Record ID: {record.get('id')}")
                        
            st.divider()

def show_about():
    st.header("About Corpus Collection Engine")
    
    st.markdown("""
    ### 🔗 Preserving Indian Culture & Diversity
    
    The **Corpus Collection Engine** is an AI-powered, open-source platform designed to preserve and celebrate 
    India's rich cultural heritage through community contributions.
    
    #### 🎯 Our Mission
    To create a comprehensive digital repository of Indian cultural knowledge, traditions, and practices 
    that can be preserved for future generations and used to build more inclusive AI systems.
    
    #### ✨ Features
    - **Multi-Category Collection**: 23+ categories including Art, Culture, Food, Literature, Music, and more
    - **Multi-Media Support**: Text, Image, Audio, and Video uploads
    - **User Dashboard**: Track your contributions and view statistics
    - **Security-First**: File validation, sanitization, and secure storage
    - **Multilingual**: Support for 12+ Indian languages
    
    #### 🌟 Categories We Support
    """, unsafe_allow_html=True)
    
    # Display categories in a grid
    cols = st.columns(4)
    categories = get_current_categories()
    for i, (category, emoji) in enumerate(categories.items()):
        with cols[i % 4]:
            st.markdown(f"**{emoji} {category}**")
    
    st.markdown("""
    #### 🤝 How to Contribute
    1. **Register/Login**: Create an account or login with existing credentials
    2. **Select Category**: Choose from our 23+ cultural categories
    3. **Choose Media Type**: Upload Text, Image, Audio, or Video content
    4. **Add Details**: Provide title, description, language, and privacy settings
    5. **Submit**: Your contribution helps preserve Indian culture!
    
    #### 🔒 Privacy & Security
    - All contributions are private by default
    - You control what content becomes public
    - Secure file storage and validation
    - No personal data is shared without consent
    
    #### 📊 Impact
    Together, we're building a comprehensive digital archive that:
    - Preserves traditional knowledge and practices
    - Supports cultural research and education
    - Helps build more inclusive AI systems
    - Celebrates India's incredible diversity
    
    ---
    
    **Join us in preserving Indian culture, one contribution at a time!** 🇮🇳
    """, unsafe_allow_html=True)

def save_contribution(contribution, content_data):
    """Save contribution to local storage"""
    # Create data directory
    data_dir = Path("data")
    uploads_dir = data_dir / "uploads"
    data_dir.mkdir(exist_ok=True)
    uploads_dir.mkdir(exist_ok=True)
    
    # Save metadata
    metadata_file = data_dir / f"{contribution['id']}_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(contribution, f, indent=2)
    
    # Save content
    if contribution['media_type'] == "Text":
        content_file = data_dir / f"{contribution['id']}.txt"
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(str(content_data))
    else:
        # For files, save the uploaded content to uploads directory
        try:
            file_extension = content_data.name.split('.')[-1] if '.' in content_data.name else 'bin'
            content_file = uploads_dir / f"{contribution['id']}.{file_extension}"
            with open(content_file, 'wb') as f:
                content_data.seek(0)  # Reset file pointer
                f.write(content_data.read())
            # Update contribution with file path
            contribution['file_path'] = str(content_file)
        except Exception as e:
            st.error(f"Error saving file: {e}")
            return False
    return True

if __name__ == "__main__":
    main()