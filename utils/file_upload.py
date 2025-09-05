import streamlit as st
import uuid
import math
from typing import Optional, Dict, Any
from config import CHUNK_SIZE, MAX_FILE_SIZE, API_TIMEOUT

def upload_file_chunked(file_data, record_data: Dict[str, Any]) -> Optional[str]:
    """Upload file using chunked upload API"""
    if not file_data:
        return None
    
    # Generate upload UUID
    upload_uuid = str(uuid.uuid4())
    filename = file_data.name
    file_size = len(file_data.getvalue())
    
    # Calculate chunks
    total_chunks = math.ceil(file_size / CHUNK_SIZE)
    
    try:
        # Upload chunks
        file_data.seek(0)
        for chunk_index in range(total_chunks):
            chunk_data = file_data.read(CHUNK_SIZE)
            
            # Prepare chunk upload
            files = {'chunk': chunk_data}
            data = {
                'filename': filename,
                'chunk_index': chunk_index,
                'total_chunks': total_chunks,
                'upload_uuid': upload_uuid
            }
            
            # Upload chunk via API
            result = st.session_state.api_client.request(
                'POST', '/records/upload/chunk',
                files=files, data=data
            )
            
            if 'error' in result:
                st.error(f"Chunk upload failed: {result['error']}")
                return None
        
        # Finalize upload and create record
        upload_data = {
            'title': record_data['title'],
            'description': record_data.get('description', ''),
            'category_id': record_data['category_id'],
            'user_id': st.session_state.user_id,
            'media_type': record_data['media_type'].lower(),
            'upload_uuid': upload_uuid,
            'filename': filename,
            'total_chunks': total_chunks,
            'release_rights': 'creator' if record_data.get('public') else 'family_or_friend',
            'language': record_data['language']
        }
        
        # Add location if provided
        if record_data.get('latitude') is not None and record_data.get('longitude') is not None:
            upload_data['latitude'] = record_data['latitude']
            upload_data['longitude'] = record_data['longitude']
        
        # Use form data for upload endpoint
        result = st.session_state.api_client.session.post(
            f"{st.session_state.api_client.base_url}/api/v1/records/upload",
            data=upload_data,
            timeout=API_TIMEOUT
        )
        
        if result.status_code == 201:
            return result.json().get('uid')
        else:
            st.error(f"Upload finalization failed: {result.status_code} - {result.text}")
            return None
        
        if 'error' not in result:
            return result.get('id')
        else:
            st.error(f"Upload finalization failed: {result['error']}")
    except Exception as e:
        st.error(f"Upload error: {str(e)}")
        return None

def validate_file_size(file_data, media_type: str) -> bool:
    """Validate file size against limits"""
    if not file_data:
        return False
    
    file_size = len(file_data.getvalue())
    max_size = MAX_FILE_SIZE.get(media_type.lower(), 0)
    
    if file_size > max_size:
        size_mb = file_size / (1024 * 1024)
        max_mb = max_size / (1024 * 1024)
        st.error(f"File too large: {size_mb:.1f}MB. Maximum allowed: {max_mb:.1f}MB")
        return False
    
    return True