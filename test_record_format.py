#!/usr/bin/env python3
"""Test the exact record format being sent to API"""

import json
from utils.category_mapper import get_category_id_from_name, get_language_enum
from utils.api_client import APIClient
from config import API_BASE_URL

def test_record_format():
    """Test the exact record format"""
    
    # Test category mapping
    print("Testing category mapping...")
    category_id = get_category_id_from_name("Fables")
    print(f"Category ID for 'Fables': {category_id}")
    
    # Test language mapping
    print("\nTesting language mapping...")
    language = get_language_enum("Hindi")
    print(f"Language enum for 'Hindi': {language}")
    
    # Create test record data
    print("\nTest record format:")
    test_record = {
        "title": "Test Text Contribution",
        "description": "This is a test text content for debugging API format",
        "category_id": category_id,
        "user_id": "12345678-1234-1234-1234-123456789012",  # Dummy UUID
        "media_type": "text",
        "language": language,
        "release_rights": "creator"
    }
    
    print(json.dumps(test_record, indent=2))
    
    # Test with location
    print("\nTest record with location:")
    test_record_with_location = test_record.copy()
    test_record_with_location["location"] = {
        "latitude": 17.385,
        "longitude": 78.4867
    }
    
    print(json.dumps(test_record_with_location, indent=2))

if __name__ == "__main__":
    test_record_format()