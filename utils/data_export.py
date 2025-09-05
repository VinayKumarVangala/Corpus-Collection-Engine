import streamlit as st
import json
from typing import Dict, Any

def export_user_data(export_format: str = "json") -> Dict[str, Any]:
    """Export user's data"""
    if not st.session_state.user_id:
        return {"error": "User not logged in"}
    
    return st.session_state.api_client.export_user_data(export_format)

def download_export_file(task_id: str) -> bytes:
    """Download exported data file"""
    # This would typically be implemented with a direct file download
    # For now, return empty bytes
    return b""

def format_export_data(data: Dict[str, Any], format_type: str = "json") -> str:
    """Format data for export"""
    if format_type.lower() == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif format_type.lower() == "csv":
        # Basic CSV formatting for contributions
        if 'contributions' in data:
            csv_lines = ["Title,Category,Media Type,Language,Date,Public"]
            for contrib in data['contributions']:
                line = f"{contrib.get('title', '')},{contrib.get('category', '')},{contrib.get('media_type', '')},{contrib.get('language', '')},{contrib.get('timestamp', '')[:10]},{contrib.get('public', False)}"
                csv_lines.append(line)
            return "\n".join(csv_lines)
    
    return str(data)