
import sys
import os

# Ensure root is in path
sys.path.append(os.getcwd())

print("Verifying imports...")

try:
    print("Importing app...")
    # diverse imports inside app.py might fail
    # We just want to see if it syntax checks and imports modules
    from app import app
    print("SUCCESS: app imported.")
except ImportError as e:
    print(f"FAIL: app import failed: {e}")
except Exception as e:
    print(f"FAIL: app failed with: {e}")

try:
    print("Importing PathFinder...")
    from modules.utils.pathfinder import PathFinder
    print("SUCCESS: PathFinder imported.")
except ImportError as e:
    print(f"FAIL: PathFinder import failed: {e}")
except Exception as e:
    print(f"FAIL: PathFinder failed with: {e}")

print("Verification complete.")
