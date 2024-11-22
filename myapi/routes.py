from typing import Callable


def route_collections(path: str, method: str, routes: dict):
        """
        Decorator to register a route.
        """
        method = method.upper()

        def decorator(func: Callable):
            if path not in routes:
                routes[path] = {}
            routes[path][method] = func
            return func

        return decorator