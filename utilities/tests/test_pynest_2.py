import nest

print("Test 2: NEST version: %s"% (nest.__version__ if hasattr(nest,'__version__') else nest.version()))
