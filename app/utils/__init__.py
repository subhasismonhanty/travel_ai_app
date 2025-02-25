"""
Utility functions and classes for the Travel AI Application
"""
import socket
from typing import Optional, Tuple

def find_available_port(start_port: int, max_attempts: int = 100) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find an available port after {max_attempts} attempts")

from .llm_handler import LLMHandler

__all__ = [
    'LLMHandler',
    'find_available_port'
] 