"""
The Chambers Protocol MCP Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A lossless linguistic mathematical syntax for high-fidelity AI alignment.
This package exposes the server and logic required to enforce
Multiplicative Grammar (U=ci^3) constraints on Large Language Models.

Copyright (c) 2025 Christopher Chambers / The Einstein Bridge.
All Rights Reserved.
"""

__version__ = "0.1.0"
__author__ = "Christopher Chambers / The Einstein Bridge"
__license__ = "Proprietary (See LICENSE)"

# Expose the server instance for easy import
# This allows external tools to say: "from chambers_protocol import server"
try:
    from .server import mcp
except ImportError:
    # Handles cases where dependencies aren't fully installed yet
    pass