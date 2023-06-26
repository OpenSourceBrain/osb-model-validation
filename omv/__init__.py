try:
    import importlib.metadata
    __version__ = importlib.metadata.version("OSBModelValidation")
except ImportError:
    import importlib_metadata
    __version__ = importlib_metadata.version("OSBModelValidation")
