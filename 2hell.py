#!/usr/bin/python3
"""Testing documentation of a module
"""
from importlib import import_module
import sys

m_imported = import_module(sys.argv[1])

if m_imported.__doc__ is None:
    print("No module documentation")
else:
    print("OK")
for f in dir(m_imported):
    if getattr(m_imported, f).__doc__ is None:
        print("-->", f)
