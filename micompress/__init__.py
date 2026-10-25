"""micompress — CLI & client for the micompress.com compression API."""

__version__ = "0.1.1"

from .api import compress_file, CompressError, DEFAULT_BASE  # noqa: F401

__all__ = ["compress_file", "CompressError", "DEFAULT_BASE", "__version__"]
