"""
Retry utilities with exponential backoff.
"""

import time
from functools import wraps
from typing import Callable, Type, Tuple, Any
import structlog

log = structlog.get_logger()


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator to retry a function with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        exceptions: Tuple of exceptions to catch

    Example:
        @retry_with_backoff(max_retries=3, base_delay=1.0)
        def fetch_data():
            # ... code that might fail
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            delay = base_delay

            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    retries += 1

                    if retries > max_retries:
                        log.error(
                            "Max retries exceeded",
                            function=func.__name__,
                            retries=retries,
                            error=str(e)
                        )
                        raise

                    log.warning(
                        "Function failed, retrying",
                        function=func.__name__,
                        attempt=retries,
                        max_retries=max_retries,
                        delay=delay,
                        error=str(e)
                    )

                    time.sleep(delay)
                    delay = min(delay * exponential_base, max_delay)

        return wrapper
    return decorator
