"""Validation engine for TES skill packages."""

from pathlib import Path
import re
from typing import List, Optional, Tuple
import yaml

from tes.models import ValidationResult

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[.*?\]\((?!https?://|mailto:)(.*?)\)")


def parse_frontmatter(content: str) -> Tuple[Optional[dict], str, Optional[str]]:
    """Extract YAML frontmatter and body from markdown content."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, content, "Missing starting '---' delimiter for YAML frontmatter"

    closing_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing_idx = i
            break

    if closing_idx == -1:
        return None, content, "Missing closing '---' delimiter for YAML frontmatter"

    yaml_text = "\n".join(lines[1:closing_idx])
    body_text = "\n".join(lines[closing_idx + 1:])

    try:
        data = yaml.safe_load(yaml_text) or {}
        if not isinstance(data, dict):
            return None, body_text, "YAML frontmatter must be a dictionary"
        return data, body_text, None
    except Exception as e:
        return None, body_text, f"Invalid YAML frontmatter: {e}"


class SkillValidator:
    """Validates skill packages for open Agent Skills compliance and integrity."""

    @classmethod
    def validate_skill_dir(cls, skill_dir: Path) -> ValidationResult:
        errors: List[str] = []
        warnings: List[str] = []
        skill_id = skill_dir.name

        if not skill_dir.exists():
            return ValidationResult(
                valid=False, skill_id=skill_id, errors=[f"Directory does not exist: {skill_dir}"]
            )

        if not skill_dir.is_dir():
            return ValidationResult(
                valid=False, skill_id=skill_id, errors=[f"Path is not a directory: {skill_dir}"]
            )

        # Check folder naming convention
        if not NAME_PATTERN.match(skill_id):
            errors.append(f"Directory name '{skill_id}' does not match required pattern: '^[a-z0-9]+(-[a-z0-9]+)*$'")

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append("Required file 'SKILL.md' is missing")
            return ValidationResult(valid=False, skill_id=skill_id, errors=errors, warnings=warnings)

        # Read and parse SKILL.md
        try:
            content = skill_md.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"Unable to read SKILL.md: {e}")
            return ValidationResult(valid=False, skill_id=skill_id, errors=errors, warnings=warnings)

        frontmatter, body, err = parse_frontmatter(content)
        if err:
            errors.append(err)
            return ValidationResult(valid=False, skill_id=skill_id, errors=errors, warnings=warnings)

        # Validate frontmatter fields
        fm_name = frontmatter.get("name")
        if not fm_name:
            errors.append("Frontmatter missing required field 'name'")
        elif fm_name != skill_id:
            errors.append(f"Frontmatter name '{fm_name}' must match directory name '{skill_id}'")

        fm_desc = frontmatter.get("description")
        if not fm_desc:
            errors.append("Frontmatter missing required field 'description'")
        elif len(str(fm_desc).strip()) < 20:
            warnings.append("Description is very short; include trigger keywords and scope details")

        # Check body sections
        if not body.strip():
            errors.append("SKILL.md body is empty")
        elif not any(line.startswith("#") for line in body.splitlines()):
            warnings.append("SKILL.md body contains no Markdown headers")

        # Check local file references
        for match in MARKDOWN_LINK_PATTERN.finditer(body):
            ref = match.group(1).split("#")[0].strip()
            if ref and not ref.startswith("/"):
                target = skill_dir / ref
                if not target.exists():
                    warnings.append(f"Referenced file does not exist: '{ref}'")

        return ValidationResult(
            valid=len(errors) == 0,
            skill_id=skill_id,
            errors=errors,
            warnings=warnings
        )
