import functools
import time
from typing import Any, Callable


def time_query(func: Callable) -> Callable:
    """Decorator to measure and print time taken by MongoDB queries."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()
        collection_name = self._get_collection_name() if hasattr(self, '_get_collection_name') else "unknown"
        print(f"{func.__name__} on collection '{collection_name}' took {end_time - start_time:.4f} seconds")
        return result

    return wrapper
