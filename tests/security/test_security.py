"""Security tests for path traversal, archive safety, and execution guards."""

from pathlib import Path
import pytest

from tes.security import (
    SecurityException,
    compute_sha256,
    is_path_contained,
    is_safe_filename,
    resolve_safe_path,
)


def test_path_containment_valid(tmp_path: Path):
    base = tmp_path / "skills"
    child = base / "engineering-core" / "SKILL.md"
    assert is_path_contained(base, child) is True


def test_path_traversal_detection_via_relative_dots(tmp_path: Path):
    base = tmp_path / "skills"
    base.mkdir()

    # Traversal escaping base directory
    with pytest.raises(SecurityException, match="Path traversal detected"):
        resolve_safe_path(base, "../../../etc/passwd")


def test_path_traversal_detection_via_absolute_path(tmp_path: Path):
    base = tmp_path / "skills"
    base.mkdir()

    with pytest.raises(SecurityException, match="Absolute path"):
        resolve_safe_path(base, "/etc/shadow")


def test_path_traversal_null_byte_injection(tmp_path: Path):
    base = tmp_path / "skills"
    base.mkdir()

    with pytest.raises(SecurityException, match="null byte"):
        resolve_safe_path(base, "skill\x00/../../etc")


def test_compute_sha256_reproducibility(tmp_path: Path):
    f = tmp_path / "test.txt"
    f.write_text("Techpronnet Engineering Skills", encoding="utf-8")
    h1 = compute_sha256(f)
    h2 = compute_sha256(f)
    assert h1 == h2
    assert len(h1) == 64


def test_is_safe_filename():
    assert is_safe_filename("SKILL.md") is True
    assert is_safe_filename("valid-name_123.py") is True
    assert is_safe_filename("..") is False
    assert is_safe_filename(".") is False
    assert is_safe_filename("bad:file*name") is False
    assert is_safe_filename("null\x00byte") is False
