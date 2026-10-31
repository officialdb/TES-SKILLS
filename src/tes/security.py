"""Security utilities and boundary defenses for TES."""

import hashlib
import os
from pathlib import Path
from typing import List, Optional, Tuple


class SecurityException(Exception):
    """Raised when an operation violates security boundaries."""
    pass


def is_path_contained(parent: Path, child: Path) -> bool:
    """Verify that child path is strictly contained within parent directory."""
    try:
        resolved_parent = parent.resolve()
        resolved_child = child.resolve()
        # Commonpath ensures child is under parent
        return os.path.commonpath([str(resolved_parent), str(resolved_child)]) == str(resolved_parent)
    except (ValueError, OSError):
        return False


def resolve_safe_path(base_dir: Path, target_relative: str | Path) -> Path:
    """Resolve a relative path against base_dir and guarantee it does not escape.
    
    Raises:
        SecurityException: If path traversal or escape is detected.
    """
    rel_str = str(target_relative).strip()
    if "\x00" in rel_str:
        raise SecurityException("Path contains forbidden null byte")

    # Disallow absolute paths when resolving relative target
    p = Path(rel_str)
    if p.is_absolute():
        raise SecurityException(f"Absolute path '{rel_str}' is forbidden for relative resolution")

    resolved_base = base_dir.resolve()
    target_path = (resolved_base / p).resolve()

    if not is_path_contained(resolved_base, target_path):
        raise SecurityException(
            f"Path traversal detected: '{rel_str}' attempts to escape '{resolved_base}'"
        )

    return target_path


def compute_sha256(file_path: Path) -> str:
    """Compute the SHA-256 digest of a file."""
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found for hash calculation: {file_path}")
    
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def is_safe_filename(name: str) -> bool:
    """Check if a filename or path component is safe."""
    if not name or name in (".", ".."):
        return False
    if "\x00" in name or "\n" in name or "\r" in name:
        return False
    # Avoid dangerous windows control characters if cross-platform
    for bad_char in [":", "*", "?", '"', "<", ">", "|"]:
        if bad_char in name:
            return False
    return True
