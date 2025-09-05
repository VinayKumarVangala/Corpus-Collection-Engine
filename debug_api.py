#!/usr/bin/env python3
"""Debug script to test API record creation"""

import json
from utils.api_client import APIClient
from config import API_BASE_URL

def test_record_creation():
    """Test record creation with minimal valid data"""
    client = APIClient(API_BASE_URL)
    
    # Test 1: Get categories
    print("Testing categories endpoint...")
    categories = client.get_categories()
    print(f"Categories result: {json.dumps(categories, indent=2)}")
    
    if 'error' in categories:
        print("Categories failed - cannot proceed")
        return
    
    # Get first category ID
    if isinstance(categories, list) and len(categories) > 0:
        category_id = categories[0]['id']
        print(f"Using category ID: {category_id}")
    else:
        print("No categories found")
        return
    
    # Test 2: Create minimal record (requires authentication)
    print("\nTesting record creation...")
    
    # This will fail without authentication, but we can see the request format
    test_record = {
        "title": "Test Record",
        "description": "Test description",
        "media_type": "text",
        "category_id": category_id,
        "user_id": "00000000-0000-0000-0000-000000000000",  # Dummy UUID
        "language": "hindi",
        "release_rights": "creator"
    }
    
    print(f"Test record data: {json.dumps(test_record, indent=2)}")
    
    result = client.create_record(test_record)
    print(f"Record creation result: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    test_record_creation()