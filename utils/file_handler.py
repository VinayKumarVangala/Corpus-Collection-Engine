import os
import hashlib
from PIL import Image
from pathlib import Path
from config import MAX_FILE_SIZES, ALLOWED_EXTENSIONS, UPLOADS_DIR

def validate_file(file, media_type):
    """Validate uploaded file according to security requirements"""
    if not file:
        return False, "No file provided"
    
    # Check file size
    file_size = len(file.getvalue())
    max_size = MAX_FILE_SIZES.get(media_type.lower(), 0)
    
    if file_size > max_size:
        return False, f"File too large. Max size: {max_size / (1024*1024):.1f}MB"
    
    # Check file extension
    file_ext = Path(file.name).suffix.lower()
    allowed_exts = ALLOWED_EXTENSIONS.get(media_type.lower(), [])
    
    if file_ext not in allowed_exts:
        return False, f"File type not allowed. Allowed: {', '.join(allowed_exts)}"
    
    return True, "Valid file"

def sanitize_image(image_file):
    """Remove EXIF data and sanitize image"""
    try:
        img = Image.open(image_file)
        # Remove EXIF data
        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(list(img.getdata()))
        return clean_img
    except Exception as e:
        raise ValueError(f"Invalid image file: {str(e)}")

def calculate_file_hash(file_content):
    """Calculate SHA-256 hash of file content"""
    return hashlib.sha256(file_content).hexdigest()

def save_file(file, contribution_id, media_type):
    """Save file to storage with security measures"""
    try:
        # Validate file
        is_valid, message = validate_file(file, media_type)
        if not is_valid:
            raise ValueError(message)
        
        # Generate secure filename
        file_ext = Path(file.name).suffix.lower()
        filename = f"{contribution_id}_{hashlib.md5(file.name.encode()).hexdigest()[:8]}{file_ext}"
        filepath = UPLOADS_DIR / filename
        
        # Save file
        if media_type.lower() == "image":
            # Sanitize image
            clean_img = sanitize_image(file)
            clean_img.save(filepath)
        else:
            # Save other file types
            with open(filepath, 'wb') as f:
                f.write(file.getvalue())
        
        return str(filepath), calculate_file_hash(file.getvalue())
    
    except Exception as e:
        raise Exception(f"Failed to save file: {str(e)}")

def get_file_info(file):
    """Get file information"""
    return {
        'name': file.name,
        'size': len(file.getvalue()),
        'type': file.type if hasattr(file, 'type') else 'unknown'
    }