# Static category mapping based on API response
CATEGORY_MAPPING = {
    "fables": "379d6867-57c1-4f57-b6ee-fb734313e538",
    "events": "7a184c41-1a49-4beb-a01a-d8dc01693b15", 
    "music": "94979e9f-4895-4cd7-8601-ad53d8099bf4",
    "places": "96e5104f-c786-4928-b932-f59f5b4ddbf0",
    "food": "833299f6-ff1c-4fde-804f-6d3b3877c76e",
    "people": "af8b7a27-00b4-4192-9fa6-90152a0640b2",
    "literature": "74b133e7-e496-4e9d-85b0-3bd5eb4c3871",
    "architecture": "94a13c20-8a03-45da-8829-10e2fe1e61a1",
    "skills": "6f6f5023-a99e-4a29-a44a-6d5acbf88085",
    "images": "4366cab1-031e-4b37-816b-311ee34461a9",
    "culture": "ab9fa2ce-1f83-4e91-b89d-cca18e8b301e",
    "flora & fauna": "5f40610f-ae47-4472-944c-cb899128ebbf",
    "education": "784ddb92-9540-4ce1-b4e4-6c1b7b18849d",
    "vegetation": "2f831ae2-f0cd-4142-8646-68dd195dfba2",
    "folk tales": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "local history": "ab7f2757-ccdf-4ef6-9850-2cdfe6e1b422",
    "food & agriculture": "d4b0cf4b-89e4-4e18-bc66-431812bb3e00",
    "newspapers older than 1980s": "1f8c68dc-10d5-4a96-991f-c33e22cfb5f7",
    "folk songs": "a2e97f91-4cf7-4f39-9e78-f7d89446a2ec",
    "traditional skills": "7cba79a5-2e5d-4f86-bfae-2aa177f0c65b",
    "local cultural history": "9d1df401-72c0-496a-867f-88e3d1f66082"
}

def get_static_category_id(category_name: str) -> str:
    """Get category ID from static mapping"""
    return CATEGORY_MAPPING.get(category_name.lower(), category_name)