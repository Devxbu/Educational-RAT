import os
import time
import shutil
from typing import Any, Callable, Dict, Tuple, Optional

from . import constants

def get_timestamp() -> str:
    """Return current timestamp in a formatted string."""
    return time.strftime("%Y%m%d_%H%M%S")

def get_file_size(file_path: str) -> int:
    """Return the size of a file in bytes."""
    return os.path.getsize(file_path)

def is_valid_path(path: str) -> bool:
    """Check if a path exists and is accessible."""
    return os.path.exists(path) and os.access(path, os.R_OK)

def ensure_directory_exists(directory: str) -> None:
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def format_file_size(size_bytes: int) -> str:
    """Convert file size in bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def get_file_hash(file_path: str) -> str:
    """Calculate MD5 hash of a file."""
    import hashlib
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def is_hidden(filepath: str) -> bool:
    """Check if a file or directory is hidden."""
    name = os.path.basename(filepath)
    return name.startswith('.') or has_hidden_attribute(filepath)

def has_hidden_attribute(filepath: str) -> bool:
    """Check if a file or directory has the hidden attribute on Windows."""
    try:
        import ctypes
        attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
        assert attrs != -1, ctypes.WinError()
        return bool(attrs & 2)  # FILE_ATTRIBUTE_HIDDEN
    except (AttributeError, ImportError, AssertionError):
        return False

def get_file_extension(file_path: str) -> str:
    """Get the file extension in lowercase."""
    _, ext = os.path.splitext(file_path)
    return ext.lower()

def is_binary_file(file_path: str) -> bool:
    """Check if a file is binary."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:  # Files with null bytes are likely binary
                return True
            # Check for non-text characters
            text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
            return bool(chunk.translate(None, text_chars))
    except Exception:
        return False
