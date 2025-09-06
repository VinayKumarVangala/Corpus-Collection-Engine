import streamlit as st
import hashlib
from datetime import datetime
from pathlib import Path
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import db
# from utils.auth import hash_password, verify_password, create_jwt_token
import hashlib
import bcrypt
from utils.file_handler import save_file, validate_file, get_file_info
from config import SUPPORTED_LANGUAGES, MAX_FILE_SIZES

# Updated categories to match the image
CATEGORIES = [
    "Fables", "Events", "Music", "Places", "Food", "People",
    "Literature", "Architecture", "Skills", "Images", "Culture", "Flora & Fauna"
]

# Page config
st.set_page_config(
    page_title="Corpus Collection Engine",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

def main():
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .category-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stat-card {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border-left: 4px solid #2196f3;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ Corpus Collection Engine</h1>
        <p>Preserving Indian Culture & Diversity</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize page state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    # Navigation Bar
    if st.session_state.user_id:
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
        
        with col1:
            st.markdown(f"**Welcome, {st.session_state.user_name}!**")
        
        with col2:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.current_page = "Home"
                st.rerun()
        
        with col3:
            if st.button("📤 Contribute", use_container_width=True):
                st.session_state.current_page = "Contribute"
                st.rerun()
        
        with col4:
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
        
        with col5:
            if st.button("🔍 Browse", use_container_width=True):
                st.session_state.current_page = "Browse"
                st.rerun()
        
        with col6:
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
        
        page = st.session_state.current_page
    else:
        col1, col2, col3 = st.columns([4, 1, 1])
        
        with col1:
            st.markdown("**Please login to access all features**")
        
        with col2:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.current_page = "Home"
                st.rerun()
        
        with col3:
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.current_page = "Login"
                st.rerun()
        
        page = st.session_state.current_page
    
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

def show_home():
    if not st.session_state.user_id:
        st.info("🚀 Welcome! Please login to start contributing to preserve Indian cultural heritage!")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://via.placeholder.com/400x200/FF6B35/FFFFFF?text=Cultural+Heritage", 
                    caption="Preserving Our Rich Heritage")
        return
    
    st.markdown(f"### Welcome back, {st.session_state.user_name}! 👋")
    
    # Quick stats
    user_contributions = db.get_user_contributions(st.session_state.user_id)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{len(user_contributions)}</h3>
            <p>Total Contributions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_size = sum(c.get('file_size', 0) for c in user_contributions)
        st.markdown(f"""
        <div class="stat-card">
            <h3>{total_size / 1024:.1f} KB</h3>
            <p>Data Contributed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        categories = len(set(c['category'] for c in user_contributions))
        st.markdown(f"""
        <div class="stat-card">
            <h3>{categories}</h3>
            <p>Categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        public_count = sum(1 for c in user_contributions if c.get('is_public', False))
        st.markdown(f"""
        <div class="stat-card">
            <h3>{public_count}</h3>
            <p>Public Items</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📂 Categories")
    st.markdown("*Choose a category to contribute content*")
    
    # Enhanced category data with descriptions matching the image
    categories_data = [
        {"name": "Fables", "icon": "📚", "desc": "Traditional stories with moral lessons and mythical characters"},
        {"name": "Events", "icon": "🎉", "desc": "Happenings, celebrations, and special occasions"},
        {"name": "Music", "icon": "🎵", "desc": "Musical content, songs, instruments, and audio experiences"},
        {"name": "Places", "icon": "🏛️", "desc": "Locations, landmarks, and geographical content"},
        {"name": "Food", "icon": "🍽️", "desc": "Culinary content, recipes, and food-related information"},
        {"name": "People", "icon": "👥", "desc": "Individuals, personalities, and human-related content"},
        {"name": "Literature", "icon": "📖", "desc": "Books, poems, writings, and literary works"},
        {"name": "Architecture", "icon": "🏗️", "desc": "Buildings, structures, and architectural designs"},
        {"name": "Skills", "icon": "⚡", "desc": "Abilities, talents, and learning materials"},
        {"name": "Images", "icon": "🖼️", "desc": "Visual content, pictures, and artistic expressions"},
        {"name": "Culture", "icon": "🎭", "desc": "Cultural traditions, customs, and practices"},
        {"name": "Flora & Fauna", "icon": "🌿", "desc": "Plants, animals, and natural life"}
    ]
    
    # Custom CSS for interactive cards matching the image design
    st.markdown("""
    <style>
    .category-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 20px 0;
    }
    .category-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px 20px;
        color: white;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .category-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .category-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }
    .category-title {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 10px;
        color: white;
    }
    .category-desc {
        font-size: 0.85rem;
        opacity: 0.9;
        line-height: 1.4;
        color: rgba(255,255,255,0.9);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create 4-column grid for categories
    cols = st.columns(4)
    
    for i, cat_data in enumerate(categories_data):
        with cols[i % 4]:
            # Create the visual card
            card_html = f"""
            <div class="category-card">
                <span class="category-icon">{cat_data['icon']}</span>
                <div class="category-title">{cat_data['name']}</div>
                <div class="category-desc">{cat_data['desc']}</div>
            </div>
            """
            
            # Display the card
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Create invisible button for functionality
            if st.button(f"Select {cat_data['name']}", key=f"cat_{i}", use_container_width=True):
                st.session_state.selected_category = cat_data['name']
                st.session_state.current_page = "Contribute"
                st.rerun()

def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 Authentication")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if email and password:
                        user = db.get_user_by_email(email)
                        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                            st.session_state.user_id = user['id']
                            st.session_state.user_email = user['email']
                            st.session_state.user_name = user['name']
                            # st.session_state.auth_token = user['id']
                            st.success("✅ Logged in successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials!")
                    else:
                        st.error("❌ Please fill all fields!")
        
        with tab2:
            with st.form("register_form"):
                reg_email = st.text_input("Email")
                reg_name = st.text_input("Display Name")
                reg_password = st.text_input("Password", type="password")
                reg_confirm = st.text_input("Confirm Password", type="password")
                submit = st.form_submit_button("Register", use_container_width=True)
                
                if submit:
                    if reg_email and reg_name and reg_password and reg_confirm:
                        if reg_password != reg_confirm:
                            st.error("❌ Passwords don't match!")
                        elif len(reg_password) < 8:
                            st.error("❌ Password must be at least 8 characters!")
                        else:
                            user_id = hashlib.md5(f"{reg_email}{datetime.now()}".encode()).hexdigest()[:12]
                            password_hash = bcrypt.hashpw(reg_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                            
                            if db.create_user(user_id, reg_email, reg_name, password_hash):
                                st.session_state.user_id = user_id
                                st.session_state.user_email = reg_email
                                st.session_state.user_name = reg_name
                                # st.session_state.auth_token = user_id
                                st.success("✅ Registered successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Email already exists!")
                    else:
                        st.error("❌ Please fill all fields!")

def show_contribute():
    if not st.session_state.user_id:
        st.warning("⚠️ Please login first!")
        return
    
    st.header("📤 Contribute Content")
    
    with st.form("contribution_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Category", CATEGORIES, 
                                  index=CATEGORIES.index(st.session_state.get('selected_category', CATEGORIES[0])) 
                                  if st.session_state.get('selected_category') in CATEGORIES else 0)
            media_type = st.selectbox("Media Type", ["Text", "Image", "Audio", "Video"])
        
        with col2:
            language = st.selectbox("Language", SUPPORTED_LANGUAGES)
            is_public = st.checkbox("Make this contribution public", value=False)
        
        title = st.text_input("Title")
        description = st.text_area("Description (optional)")
        
        # Content input based on media type
        content_data = None
        file_info = None
        
        if media_type == "Text":
            content_data = st.text_area("Enter your text content", height=200)
            if content_data:
                file_info = {'size': len(content_data.encode('utf-8')), 'type': 'text/plain'}
        else:
            file_types = {
                "Image": ['png', 'jpg', 'jpeg', 'gif', 'webp'],
                "Audio": ['mp3', 'wav', 'ogg', 'm4a'],
                "Video": ['mp4', 'avi', 'mov', 'mkv', 'webm']
            }
            
            uploaded_file = st.file_uploader(
                f"Upload {media_type}", 
                type=file_types[media_type],
                help=f"Max size: {MAX_FILE_SIZES[media_type.lower()] / (1024*1024):.0f}MB"
            )
            
            if uploaded_file:
                content_data = uploaded_file
                file_info = get_file_info(uploaded_file)
                
                # Show preview
                if media_type == "Image":
                    st.image(uploaded_file, caption="Preview", width=300)
                elif media_type == "Audio":
                    st.audio(uploaded_file)
                elif media_type == "Video":
                    st.video(uploaded_file)
        
        # File validation info
        if file_info:
            max_size = MAX_FILE_SIZES[media_type.lower()]
            if file_info['size'] > max_size:
                st.error(f"❌ File too large! Max size: {max_size / (1024*1024):.1f}MB")
            else:
                st.success(f"✅ File size: {file_info['size'] / 1024:.1f}KB")
        
        submit = st.form_submit_button("🚀 Submit Contribution", use_container_width=True)
        
        if submit:
            if not title:
                st.error("❌ Please provide a title!")
            elif not content_data:
                st.error("❌ Please provide content!")
            else:
                try:
                    # Create contribution
                    contribution_id = hashlib.md5(f"{st.session_state.user_id}{datetime.now()}".encode()).hexdigest()[:12]
                    
                    contribution_data = {
                        'id': contribution_id,
                        'user_id': st.session_state.user_id,
                        'category': category,
                        'media_type': media_type,
                        'title': title,
                        'description': description,
                        'language': language,
                        'is_public': is_public,
                        'file_size': file_info['size'] if file_info else 0
                    }
                    
                    # Save file if not text
                    if media_type != "Text":
                        file_path, file_hash = save_file(content_data, contribution_id, media_type)
                        contribution_data['file_path'] = file_path
                        contribution_data['file_hash'] = file_hash
                    else:
                        # Save text content
                        text_path = Path("data/uploads") / f"{contribution_id}.txt"
                        with open(text_path, 'w', encoding='utf-8') as f:
                            f.write(content_data)
                        contribution_data['file_path'] = str(text_path)
                        contribution_data['file_hash'] = hashlib.sha256(content_data.encode()).hexdigest()
                    
                    # Save to database
                    db.create_contribution(contribution_data)
                    
                    st.success("🎉 Contribution submitted successfully!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def show_dashboard():
    if not st.session_state.user_id:
        st.warning("⚠️ Please login first!")
        return
    
    st.header("📊 Your Dashboard")
    
    user_contributions = db.get_user_contributions(st.session_state.user_id)
    
    if not user_contributions:
        st.info("📝 No contributions yet. Start contributing to see your stats!")
        if st.button("🚀 Start Contributing"):
            st.session_state.current_page = "Contribute"
            st.rerun()
        return
    
    # Detailed stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Contributions", len(user_contributions))
    
    with col2:
        total_size = sum(c.get('file_size', 0) for c in user_contributions)
        st.metric("Total Size", f"{total_size / 1024:.1f} KB")
    
    with col3:
        categories = len(set(c['category'] for c in user_contributions))
        st.metric("Categories Used", categories)
    
    with col4:
        public_count = sum(1 for c in user_contributions if c.get('is_public', False))
        st.metric("Public Contributions", public_count)
    
    # Media type breakdown
    st.subheader("📈 Contributions by Media Type")
    media_counts = {}
    for contrib in user_contributions:
        media_type = contrib['media_type']
        media_counts[media_type] = media_counts.get(media_type, 0) + 1
    
    if media_counts:
        st.bar_chart(media_counts)
    
    # Recent contributions table
    st.subheader("📋 Recent Contributions")
    for contrib in user_contributions[:10]:
        with st.expander(f"{contrib['title']} ({contrib['media_type']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Category:** {contrib['category']}")
                st.write(f"**Language:** {contrib['language']}")
                st.write(f"**Size:** {contrib.get('file_size', 0) / 1024:.1f} KB")
            with col2:
                st.write(f"**Created:** {contrib['created_at'][:19]}")
                st.write(f"**Public:** {'Yes' if contrib.get('is_public') else 'No'}")
                if contrib.get('description'):
                    st.write(f"**Description:** {contrib['description']}")

def show_browse():
    st.header("🔍 Browse Public Contributions")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox("Category", ["All"] + CATEGORIES)
    with col2:
        filter_media = st.selectbox("Media Type", ["All", "Text", "Image", "Audio", "Video"])
    with col3:
        filter_language = st.selectbox("Language", ["All"] + SUPPORTED_LANGUAGES)
    
    # Get filtered contributions
    contributions = db.get_public_contributions(
        category=filter_category if filter_category != "All" else None,
        media_type=filter_media if filter_media != "All" else None,
        language=filter_language if filter_language != "All" else None
    )
    
    st.write(f"📊 Found {len(contributions)} public contributions")
    
    if not contributions:
        st.info("No public contributions found with the selected filters.")
        return
    
    # Display contributions
    for contrib in contributions:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{contrib['title']}**")
                if contrib.get('description'):
                    st.write(contrib['description'])
                st.caption(f"Category: {contrib['category']} | Language: {contrib['language']}")
            
            with col2:
                st.write(f"📁 {contrib['media_type']}")
                st.write(f"📏 {contrib.get('file_size', 0) / 1024:.1f} KB")
            
            with col3:
                st.write(f"📅 {contrib['created_at'][:10]}")
            
            st.divider()

def logout_user():
    """Logout current user"""
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.user_name = None
    if 'auth_token' in st.session_state:
        del st.session_state.auth_token
    st.rerun()

if __name__ == "__main__":
    main()