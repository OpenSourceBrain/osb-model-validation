import nest

print("Test 1: NEST version: %s"% (nest.__version__ if hasattr(nest,'__version__') else nest.version()))
