#!/usr/bin/env python
"""Test script to verify orcatools installation."""

import sys
import os

try:
    import orcatools

    print("✓ orcatools imported successfully")
    print(f"  Package location: {os.path.dirname(orcatools.__file__)}")

    from orcatools.inp import ORCAINP

    print("✓ ORCAINP imported successfully")

    from orcatools.out import ORCAOUT

    print("✓ ORCAOUT imported successfully")

    from orcatools.tools import get_coordinates_from_xyz, interpolate

    print("✓ orcatools.tools functions imported successfully")

    print("\n✅ All imports successful! Package is properly installed.")
    sys.exit(0)

except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)
