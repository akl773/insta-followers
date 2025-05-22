import time
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable)


def time_query(func: F) -> F:
    """
    Decorator to measure and log the execution time of MongoDB queries.
    Handles both instance methods and class methods.
    """

    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        # Determine if this is a class method or instance method
        if args and hasattr(args[0], '__name__'):  # Class method (first arg is the class)
            cls = args[0]
            try:
                collection_name = cls._get_collection_name_cls()
            except:
                collection_name = cls.__name__.lower()
        elif args:  # Instance method (first arg is self)
            self = args[0]
            try:
                collection_name = self._get_collection_name()
            except:
                collection_name = "unknown"
        else:
            collection_name = "unknown"

        print(f"{func.__name__} on collection '{collection_name}' took {end_time - start_time:.4f} seconds")
        return result

    return wrapper
