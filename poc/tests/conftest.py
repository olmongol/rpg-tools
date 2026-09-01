"""pytest bootstrap: put the PoC package root on sys.path."""
import os
import sys

# conftest is at poc/tests/conftest.py; package root is poc/
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
