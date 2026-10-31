"""Data models and schemas for TES."""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class Scope(str, Enum):
    PROJECT = "project"
    GLOBAL = "global"


class AdapterTarget(str, Enum):
    AUTO = "auto"
    HERMES = "hermes"
    OPENCODE = "opencode"
    CODEX = "codex"
    CLAUDE_CODE = "claude-code"
    GEMINI_CLI = "gemini-cli"
    GENERIC = "generic"


class SkillMetadata(BaseModel):
    id: str = Field(..., pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    name: str
    version: str = "1.0.0"
    category: str = "engineering"
    description: str
    path: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    compatibility: List[str] = Field(default_factory=list)


class BundleMetadata(BaseModel):
    id: str = Field(..., pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    name: str
    description: str
    skills: List[str] = Field(default_factory=list)


class InstalledSkillManifest(BaseModel):
    skill_id: str
    version: str
    installed_at: str
    scope: Scope
    target: str
    managed_files: List[str] = Field(default_factory=list)
    hashes: Dict[str, str] = Field(default_factory=dict)


class TargetManifest(BaseModel):
    version: int = 1
    skills: Dict[str, InstalledSkillManifest] = Field(default_factory=dict)


class ValidationResult(BaseModel):
    valid: bool
    skill_id: str
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
