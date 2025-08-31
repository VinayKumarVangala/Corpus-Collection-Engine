import streamlit as st
import json
import hashlib
from datetime import datetime
from pathlib import Path
import os
import bcrypt

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

# Categories with matching emojis
CATEGORIES = {
    "Art": "🎨",
    "Meme": "😂", 
    "Culture": "🏛️",
    "Food": "🍛",
    "Fables": "📚",
    "Events": "🎉",
    "Music": "🎵",
    "People": "👥",
    "Literature": "📖",
    "Architecture": "🏗️",
    "Skills": "⚡",
    "Images": "📸",
    "Videos": "🎬",
    "Flora": "🌸",
    "Fauna": "🦋",
    "Education": "🎓",
    "Vegetation": "🌿",
    "Folk Talks": "🗣️",
    "Traditional Skills": "🛠️",
    "Local History": "📜",
    "Local Locations": "📍",
    "Food & Agriculture": "🌾",
    "Newspapers": "📰"
}

MEDIA_TYPES = ["Text", "Image", "Audio", "Video"]

# Data persistence functions
def load_users():
    """Load users from persistent storage"""
    users_file = Path("data/users.json")
    if users_file.exists():
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to persistent storage"""
    Path("data").mkdir(exist_ok=True)
    with open("data/users.json", 'w') as f:
        json.dump(users, f, indent=2)

def load_contributions():
    """Load contributions from persistent storage"""
    contrib_file = Path("data/contributions.json")
    if contrib_file.exists():
        with open(contrib_file, 'r') as f:
            return json.load(f)
    return []

def save_contributions(contributions):
    """Save contributions to persistent storage"""
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
                st.session_state.user_email = session_data.get('user_email')
                st.session_state.user_name = session_data.get('user_name')
                st.session_state.page = session_data.get('page', 'Home')
        except:
            pass

def save_user_session():
    """Save current user session to persistent storage"""
    if st.session_state.user_id:
        session_data = {
            'user_id': st.session_state.user_id,
            'user_email': st.session_state.user_email,
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

# Initialize session state with persistent data
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'contributions' not in st.session_state:
    st.session_state.contributions = load_contributions()
if 'offline_queue' not in st.session_state:
    st.session_state.offline_queue = []
if 'registered_users' not in st.session_state:
    st.session_state.registered_users = load_users()
if 'page_history' not in st.session_state:
    st.session_state.page_history = []

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
        nav_cols = st.columns([1, 1, 1, 1, 1, 0.5])
        
        for i, option in enumerate(nav_options):
            with nav_cols[i]:
                if st.button(option, key=f"nav_{option}", use_container_width=True, 
                           type="primary" if option == st.session_state.page else "secondary"):
                    if st.session_state.page != option:
                        st.session_state.page = option
                        save_user_session()
                        st.rerun()
        
        # Logout button
        with nav_cols[5]:
            if st.button("Logout", key="logout_btn", use_container_width=True, type="secondary"):
                # Clear session but keep persistent data
                clear_user_session()
                st.session_state.user_id = None
                st.session_state.user_name = None
                st.session_state.user_email = None
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
        "Art": "Creative works, paintings, and artistic expressions",
        "Meme": "Humorous content and cultural references", 
        "Culture": "Cultural traditions, customs, and practices",
        "Food": "Culinary content, recipes, and food-related information",
        "Fables": "Traditional stories with moral lessons and mythical characters",
        "Events": "Happenings, celebrations, and special occasions",
        "Music": "Musical content, songs, instruments, and audio experiences",
        "People": "Individuals, personalities, and human-related content",
        "Literature": "Books, poems, writings, and literary works",
        "Architecture": "Buildings, structures, and architectural designs",
        "Skills": "Abilities, talents, and learning",
        "Images": "Visual content, pictures, and photography",
        "Videos": "Video content and multimedia experiences",
        "Flora": "Plants, flowers, and botanical content",
        "Fauna": "Animals, wildlife, and zoological content",
        "Education": "Learning materials and educational content",
        "Vegetation": "Plant life, gardens, and natural growth",
        "Folk Talks": "Traditional conversations and oral traditions",
        "Traditional Skills": "Heritage crafts and ancestral knowledge",
        "Local History": "Regional stories and historical accounts",
        "Local Locations": "Places, landmarks, and geographical content",
        "Food & Agriculture": "Farming, crops, and agricultural practices",
        "Newspapers": "News articles and journalistic content"
    }
    
    # Category grid - 4 columns per row
    cols_per_row = 4
    categories_list = list(CATEGORIES.items())
    
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
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login", type="primary"):
            if email and password:
                # Check if user is registered
                if email in st.session_state.registered_users:
                    stored_password_hash = st.session_state.registered_users[email]['password']
                    if verify_password(password, stored_password_hash):
                        st.session_state.user_id = hashlib.md5(email.encode()).hexdigest()[:8]
                        st.session_state.user_email = email
                        st.session_state.user_name = st.session_state.registered_users[email]['name']
                        st.session_state.page = "Home"
                        save_user_session()  # Save session for persistence
                        st.success("Logged in successfully!")
                        st.balloons()
                        # Force page refresh by using experimental_rerun
                        try:
                            st.experimental_rerun()
                        except:
                            st.rerun()
                    else:
                        st.error("Invalid password!")
                else:
                    st.error("User not registered. Please register first.")
            else:
                st.error("Please enter both email and password.")
    
    with tab2:
        reg_email = st.text_input("Email", key="reg_email")
        reg_name = st.text_input("Display Name")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register", type="primary"):
            if reg_email and reg_name and reg_password:
                if reg_email not in st.session_state.registered_users:
                    # Store user credentials with hashed password
                    st.session_state.registered_users[reg_email] = {
                        'name': reg_name,
                        'password': hash_password(reg_password),
                        'created_at': datetime.now().isoformat()
                    }
                    save_users(st.session_state.registered_users)
                    st.session_state.user_id = hashlib.md5(reg_email.encode()).hexdigest()[:8]
                    st.session_state.user_email = reg_email
                    st.session_state.user_name = reg_name
                    st.session_state.page = "Home"
                    save_user_session()  # Save session for persistence
                    st.success("Registered successfully!")
                    st.balloons()
                    # Force page refresh
                    try:
                        st.experimental_rerun()
                    except:
                        st.rerun()
                else:
                    st.error("Email already registered. Please use a different email or login.")
            else:
                st.error("Please fill in all fields.")

def show_contribute():
    if not st.session_state.user_id:
        st.warning("Please login first!")
        return
    
    st.header("Contribute Content")
    
    # Step 1: Category Selection
    if 'selected_category' in st.session_state and st.session_state.selected_category:
        category = st.selectbox("Select Category", list(CATEGORIES.keys()), 
                               index=list(CATEGORIES.keys()).index(st.session_state.selected_category))
    else:
        category = st.selectbox("Select Category", list(CATEGORIES.keys()))
    
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
    
    # Step 5: Submit
    if st.button("Submit Contribution", type="primary"):
        if content_data:
            contribution = {
                "id": hashlib.md5(f"{st.session_state.user_id}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
                "user_id": st.session_state.user_id,
                "category": category,
                "media_type": media_type,
                "title": title or f"{media_type} contribution",
                "description": description,
                "language": language,
                "public": public_consent,
                "timestamp": datetime.now().isoformat(),
                "size": len(str(content_data)) if media_type == "Text" else len(content_data.getvalue()) if hasattr(content_data, 'getvalue') else 0
            }
            
            # Add to contributions
            st.session_state.contributions.append(contribution)
            
            # Save content and update persistent storage
            if save_contribution(contribution, content_data):
                save_contributions(st.session_state.contributions)
                st.success("Contribution submitted successfully!")
                st.balloons()
            else:
                st.error("Failed to save contribution. Please try again.")
        else:
            st.error("Please provide content before submitting!")

def show_dashboard():
    if not st.session_state.user_id:
        st.warning("Please login first!")
        return
    
    st.header("Your Dashboard")
    
    user_contributions = [c for c in st.session_state.contributions if c['user_id'] == st.session_state.user_id]
    
    if not user_contributions:
        st.info("No contributions yet. Start contributing to see your stats!")
        return
    
    # Stats with colorful cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 6px 20px rgba(52, 152, 219, 0.3); border: 1px solid #e9ecef;">
            <h3 style="color: white; margin: 0; font-size: 28px;">📊</h3>
            <h2 style="color: white; margin: 10px 0; font-size: 32px;">{}</h2>
            <p style="color: white; margin: 0; font-size: 14px;">Total Contributions</p>
        </div>
        """.format(len(user_contributions)), unsafe_allow_html=True)
    
    with col2:
        total_size = sum(c.get('size', 0) for c in user_contributions)
        formatted_size = format_file_size(total_size)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 6px 20px rgba(46, 204, 113, 0.3); border: 1px solid #e9ecef;">
            <h3 style="color: white; margin: 0; font-size: 28px;">💾</h3>
            <h2 style="color: white; margin: 10px 0; font-size: 32px;">{}</h2>
            <p style="color: white; margin: 0; font-size: 14px;">Total Size</p>
        </div>
        """.format(formatted_size), unsafe_allow_html=True)
    
    with col3:
        categories = len(set(c['category'] for c in user_contributions))
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 6px 20px rgba(231, 76, 60, 0.3); border: 1px solid #e9ecef;">
            <h3 style="color: white; margin: 0; font-size: 28px;">📂</h3>
            <h2 style="color: white; margin: 10px 0; font-size: 32px;">{}</h2>
            <p style="color: white; margin: 0; font-size: 14px;">Categories</p>
        </div>
        """.format(categories), unsafe_allow_html=True)
    
    with col4:
        public_count = sum(1 for c in user_contributions if c.get('public', False))
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 6px 20px rgba(243, 156, 18, 0.3); border: 1px solid #e9ecef;">
            <h3 style="color: white; margin: 0; font-size: 28px;">🌍</h3>
            <h2 style="color: white; margin: 10px 0; font-size: 32px;">{}</h2>
            <p style="color: white; margin: 0; font-size: 14px;">Public Contributions</p>
        </div>
        """.format(public_count), unsafe_allow_html=True)
    
    # Media type breakdown
    st.subheader("Contributions by Media Type")
    media_counts = {}
    for contrib in user_contributions:
        media_type = contrib['media_type']
        media_counts[media_type] = media_counts.get(media_type, 0) + 1
    
    if media_counts:
        st.bar_chart(media_counts)
    
    # Recent contributions
    st.subheader("Recent Contributions")
    for contrib in sorted(user_contributions, key=lambda x: x['timestamp'], reverse=True)[:5]:
        with st.expander(f"{contrib['title']} ({contrib['media_type']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Category:** {contrib['category']}")
                st.write(f"**Language:** {contrib['language']}")
            with col2:
                st.write(f"**Date:** {contrib['timestamp'][:10]}")
                st.write(f"**Public:** {'Yes' if contrib.get('public') else 'No'}")

def show_browse():
    st.header("Browse Contributions")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(CATEGORIES.keys()))
    with col2:
        filter_media = st.selectbox("Filter by Media Type", ["All"] + MEDIA_TYPES)
    with col3:
        filter_language = st.selectbox("Filter by Language", ["All", "English", "Hindi", "Telugu", "Tamil", "Kannada"])
    
    # Get public contributions
    public_contributions = [c for c in st.session_state.contributions if c.get('public', False)]
    
    # Apply filters
    filtered = public_contributions
    if filter_category != "All":
        filtered = [c for c in filtered if c['category'] == filter_category]
    if filter_media != "All":
        filtered = [c for c in filtered if c['media_type'] == filter_media]
    if filter_language != "All":
        filtered = [c for c in filtered if c['language'] == filter_language]
    
    st.write(f"Found {len(filtered)} contributions")
    
    # Display contributions
    for contrib in filtered:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{contrib['title']}**")
                st.write(f"Category: {contrib['category']} | Type: {contrib['media_type']} | Language: {contrib['language']}")
                if contrib.get('description'):
                    st.write(contrib['description'])
            with col2:
                st.write(f"📅 {contrib['timestamp'][:10]}")
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
    for i, (category, emoji) in enumerate(CATEGORIES.items()):
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