#!/usr/bin/env python3
"""
Initialize data storage for Corpus Collection Engine
"""

import json
from pathlib import Path

def init_data_storage():
    """Initialize data storage structure"""
    # Create directories
    directories = [
        "data",
        "data/uploads",
        "data/metadata"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Initialize empty data files if they don't exist
    users_file = Path("data/users.json")
    if not users_file.exists():
        with open(users_file, 'w') as f:
            json.dump({}, f, indent=2)
        print("Created users.json")
    
    contributions_file = Path("data/contributions.json")
    if not contributions_file.exists():
        with open(contributions_file, 'w') as f:
            json.dump([], f, indent=2)
        print("Created contributions.json")
    
    print("Data storage initialized successfully!")

if __name__ == "__main__":
    init_data_storage()