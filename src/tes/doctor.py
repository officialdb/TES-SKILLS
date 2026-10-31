"""Diagnostic health check engine for TES."""

import os
from pathlib import Path
import platform
import sys
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from tes.adapters import get_all_adapters
from tes.config import find_project_root, get_registry_dir, get_user_home
from tes.models import Scope
from tes.registry import Registry


class DoctorCheckItem(BaseModel):
    category: str
    name: str
    passed: bool
    details: str
    recommendation: Optional[str] = None


class DoctorReport(BaseModel):
    python_version: str
    python_executable: str
    platform_info: str
    project_root: str
    checks: List[DoctorCheckItem]
    issues_count: int
    all_healthy: bool


class Doctor:
    """Diagnoses environment health, write permissions, and manifest integrity."""

    @classmethod
    def run_diagnostics(cls, project_root: Optional[Path] = None) -> DoctorReport:
        root = project_root or find_project_root()
        checks: List[DoctorCheckItem] = []

        # 1. Python version check
        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        py_ok = sys.version_info >= (3, 10)
        checks.append(
            DoctorCheckItem(
                category="Runtime",
                name="Python Version >= 3.10",
                passed=py_ok,
                details=f"Current Python: {py_ver}",
                recommendation=None if py_ok else "Upgrade Python to 3.10 or newer."
            )
        )

        # 2. Registry files check
        reg_dir = get_registry_dir()
        skills_yaml = reg_dir / "skills.yaml"
        bundles_yaml = reg_dir / "bundles.yaml"
        reg_ok = skills_yaml.exists() and bundles_yaml.exists()
        reg_details = f"Registry at: {reg_dir}"
        if not reg_ok:
            reg_details += " (Missing skills.yaml or bundles.yaml)"
        checks.append(
            DoctorCheckItem(
                category="Registry",
                name="Registry Files Present",
                passed=reg_ok,
                details=reg_details,
                recommendation=None if reg_ok else "Verify TES installation or set TES_ROOT."
            )
        )

        if reg_ok:
            try:
                reg = Registry(reg_dir)
                reg.load()
                s_count = len(reg.list_skills())
                b_count = len(reg.list_bundles())
                checks.append(
                    DoctorCheckItem(
                        category="Registry",
                        name="Registry Schema Integrity",
                        passed=True,
                        details=f"Loaded {s_count} skills and {b_count} bundles cleanly."
                    )
                )
            except Exception as e:
                checks.append(
                    DoctorCheckItem(
                        category="Registry",
                        name="Registry Schema Integrity",
                        passed=False,
                        details=f"Registry parsing error: {e}",
                        recommendation="Check syntax of skills.yaml and bundles.yaml."
                    )
                )

        # 3. Check adapters write access & directories
        adapters = get_all_adapters()
        for adapter in adapters:
            for scope in [Scope.PROJECT, Scope.GLOBAL]:
                try:
                    status = adapter.validate_target(scope, root)
                    writable = status["writable"]
                    checks.append(
                        DoctorCheckItem(
                            category=f"Adapter: {adapter.name}",
                            name=f"{scope.value.capitalize()} Scope Write Permission",
                            passed=writable,
                            details=f"Path: {status['path']} (Writable: {writable})",
                            recommendation=None if writable else f"Grant write permissions to {status['path']}"
                        )
                    )
                except Exception as e:
                    checks.append(
                        DoctorCheckItem(
                            category=f"Adapter: {adapter.name}",
                            name=f"{scope.value.capitalize()} Scope Check",
                            passed=False,
                            details=f"Error evaluating target: {e}"
                        )
                    )

        issues = [c for c in checks if not c.passed]

        return DoctorReport(
            python_version=py_ver,
            python_executable=sys.executable,
            platform_info=f"{platform.system()} {platform.release()}",
            project_root=str(root),
            checks=checks,
            issues_count=len(issues),
            all_healthy=len(issues) == 0
        )
