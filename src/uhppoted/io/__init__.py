"""
Python wrapper around the request/response API for the UHPPOTE TCP/IP access controllers. The IO library
implements a simpler API that returns the unvalidated response from the controller.
"""

from .set_firstcard import set_firstcard
from .set_firstcard import set_firstcard_async

# public API
__all__ = [
    "set_firstcard",
    "set_firstcard_async",
]
