import eden_simulator

print(
    "EDEN version: %s"
    % (eden_simulator.__version__ if hasattr(eden_simulator, "__version__") else "???")
)
