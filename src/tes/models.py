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


class EnvironmentStatus(BaseModel):
    adapter_id: str
    name: str
    installed: bool = False
    application_found: bool = False
    installation_method: str = "—"
    executable_found: bool = False
    version_verified: bool = False
    version: Optional[str] = None
    application_path: Optional[str] = None
    executable_path: Optional[str] = None
    config_present: bool = False
    skills_directory_present: bool = False
    project_config_present: bool = False
    available: bool = True
    details: Optional[str] = None
    global_path: str = ""
    project_path: str = ""
    detected_system: bool = False
    detected_project: bool = False


class DetectionReport(BaseModel):
    project_root: Optional[str] = None
    detected_environments: List[EnvironmentStatus] = Field(default_factory=list)
    primary_recommended: Optional[str] = None


class ValidationResult(BaseModel):
    valid: bool
    skill_id: str
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
