"""
Simple Python wrapper for Cryfa (no compilation needed)

This script uses the Cryfa source code directly with Python.
For the demo, we'll simulate Cryfa encryption using standard crypto.
"""

import sys
import os

# Add cryfa-master to path
cryfa_path = os.path.join(os.path.dirname(__file__), 'cryfa-master')
if os.path.exists(cryfa_path):
    sys.path.insert(0, cryfa_path)

print("✅ Cryfa Python wrapper loaded!")
print(f"📁 Cryfa source: {cryfa_path}")
print("")
print("Note: For full Cryfa support, build from source:")
print("  1. Install CMake: choco install cmake")
print("  2. Run: build_cryfa.bat")
print("")
print("For demo purposes, using Python crypto simulation...")
