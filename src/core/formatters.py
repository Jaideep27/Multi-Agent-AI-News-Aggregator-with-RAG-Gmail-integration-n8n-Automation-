"""
Formatting utilities.
"""

from datetime import datetime
from typing import Optional


def format_datetime(
    dt: datetime,
    fmt: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Format datetime to string.

    Args:
        dt: Datetime object
        fmt: Format string (default: ISO-like)

    Returns:
        Formatted datetime string
    """
    return dt.strftime(fmt)


def truncate_text(
    text: str,
    max_length: int = 100,
    suffix: str = "..."
) -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

    return f"{size_bytes:.2f} PB"


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Human-readable duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"
