import sys
import os

print("Python sys.path:")
for p in sys.path:
    print(f"  {p}")

print("\nCurrent directory:", os.getcwd())
print("\nDirectory contents:", os.listdir("."))
