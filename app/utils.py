import socket
from typing import Optional
import streamlit as st

def find_available_port(start_port: int = 8000, max_attempts: int = 100) -> Optional[int]:
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

def get_chat_response(assistant, message: str, category: Optional[str] = None) -> str:
    """Get response from AI assistant"""
    try:
        if category:
            prompt = f"Focus on {category} for this query: {message}"
        else:
            prompt = message
            
        response = assistant.chat(prompt)
        if hasattr(response, '__iter__'):
            return ' '.join(map(str, response))
        return str(response)
    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
        return f"Error: {str(e)}" 