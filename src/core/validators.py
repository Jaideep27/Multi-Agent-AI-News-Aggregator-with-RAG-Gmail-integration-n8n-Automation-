"""
Validation utilities.
"""

import re
from typing import Optional
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.

    Args:
        url: URL string to validate

    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_email(email: str) -> bool:
    """
    Validate if a string is a valid email address.

    Args:
        email: Email string to validate

    Returns:
        True if valid email, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_api_key(api_key: str, min_length: int = 20) -> bool:
    """
    Validate if a string is a valid API key.

    Args:
        api_key: API key to validate
        min_length: Minimum length for API key

    Returns:
        True if valid API key, False otherwise
    """
    return bool(api_key and len(api_key.strip()) >= min_length)
