import streamlit as st
from utils.permissions import is_admin, has_permission
from utils.categories import get_categories

def show_admin_panel():
    """Admin panel for system management"""
    if not is_admin():
        st.error("Access denied. Admin privileges required.")
        return
    
    st.header("🔧 Admin Panel")
    
    tab1, tab2, tab3 = st.tabs(["Users", "Categories", "System"])
    
    with tab1:
        show_user_management()
    
    with tab2:
        show_category_management()
    
    with tab3:
        show_system_stats()

def show_user_management():
    """User management interface"""
    st.subheader("👥 User Management")
    
    # Get all users
    users_result = st.session_state.api_client.request('GET', '/users/')
    
    if 'error' not in users_result:
        st.write(f"Total Users: {len(users_result)}")
        
        # User list
        for user in users_result[:10]:  # Show first 10
            with st.expander(f"{user.get('name', 'Unknown')} - {user.get('phone', 'N/A')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**ID:** {user.get('id')}")
                    st.write(f"**Phone:** {user.get('phone', 'N/A')}")
                    st.write(f"**Created:** {user.get('created_at', 'N/A')[:10]}")
                
                with col2:
                    # Role management
                    if st.button(f"Manage Roles", key=f"roles_{user.get('id')}"):
                        st.info("Role management interface would go here")

def show_category_management():
    """Category management interface"""
    st.subheader("📂 Category Management")
    
    # Get categories
    categories_result = st.session_state.api_client.get_categories()
    
    if 'error' not in categories_result:
        st.write(f"Total Categories: {len(categories_result)}")
        
        # Add new category
        with st.expander("➕ Add New Category"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Category Name")
                new_title = st.text_input("Category Title")
            
            with col2:
                new_description = st.text_area("Description")
                published = st.checkbox("Published", value=True)
            
            if st.button("Create Category"):
                category_data = {
                    "name": new_name,
                    "title": new_title,
                    "description": new_description,
                    "published": published
                }
                
                result = st.session_state.api_client.request('POST', '/categories/', json=category_data)
                
                if 'error' not in result:
                    st.success("Category created successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to create category: {result['error']}")

def show_system_stats():
    """System statistics and monitoring"""
    st.subheader("📊 System Statistics")
    
    # Get system stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Total users
        users_result = st.session_state.api_client.request('GET', '/users/')
        user_count = len(users_result) if 'error' not in users_result else 0
        
        st.metric("Total Users", user_count)
    
    with col2:
        # Total records
        records_result = st.session_state.api_client.get_records()
        record_count = len(records_result) if 'error' not in records_result else 0
        
        st.metric("Total Records", record_count)
    
    with col3:
        # Total categories
        categories_result = st.session_state.api_client.get_categories()
        category_count = len(categories_result) if 'error' not in categories_result else 0
        
        st.metric("Total Categories", category_count)