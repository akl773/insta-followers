import functools
import time
from typing import Callable


def time_query(func: Callable) -> Callable:
    """Decorator to measure and print time taken by MongoDB queries."""

    @functools.wraps(func)
    def wrapper(self, collection_name: str, *args, **kwargs) -> Any:
        start_time = time.time()
        result = func(self, collection_name, *args, **kwargs)
        execution_time = time.time() - start_time
        print(f"⏱️ Query time for {func.__name__} on '{collection_name}': {execution_time:.4f} seconds\n")
        return result

    return wrapper
