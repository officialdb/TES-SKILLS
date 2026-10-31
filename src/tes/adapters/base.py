"""Abstract base adapter for AI coding agent environments."""

from abc import ABC, abstractmethod
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any, Dict, List, Optional, Tuple

from tes.config import MANIFEST_FILE_NAME, find_project_root, get_user_home
from tes.discovery import (
    ApplicationDiscoveryEngine,
    ApplicationSpec,
    CLIDiscoveryProvider,
    DesktopDiscoveryProvider,
    DiscoveryResult,
    InstallationMethod,
    PackageManagerDiscoveryProvider,
)
from tes.models import EnvironmentStatus, InstalledSkillManifest, Scope, TargetManifest


class BaseAdapter(ABC):
    """Abstract base class that all environment adapters must implement."""

    name: str
    target_id: str
    default_project_rel_path: str
    default_global_rel_path: str

    executable_name: Optional[str] = None
    alternative_executables: List[str] = []
    version_args: List[str] = ["--version"]
    is_application: bool = True

    # Multi-method discovery metadata
    desktop_names: List[str] = []
    desktop_file_patterns: List[str] = []
    known_app_dirs: List[Path] = []
    known_binaries: List[Path] = []
    package_names: List[str] = []
    flatpak_ids: List[str] = []
    snap_names: List[str] = []
    version_file_rel_paths: List[str] = []

    def get_app_spec(self) -> ApplicationSpec:
        """Construct the ApplicationSpec for multi-method discovery."""
        cli_cmds = [self.executable_name] if self.executable_name else []
        return ApplicationSpec(
            adapter_id=self.target_id,
            display_name=self.name,
            cli_commands=cli_cmds,
            cli_version_args=self.version_args,
            desktop_names=self.desktop_names or [self.name],
            desktop_file_patterns=self.desktop_file_patterns,
            known_app_dirs=self.known_app_dirs,
            known_binaries=self.known_binaries,
            package_names=self.package_names,
            flatpak_ids=self.flatpak_ids,
            snap_names=self.snap_names,
            version_file_rel_paths=self.version_file_rel_paths,
            is_standalone_application=self.is_application,
        )

    def find_executable(self) -> Optional[Path]:
        """Discover the CLI executable on PATH or known locations."""
        spec = self.get_app_spec()
        found, exe_path, _, _ = CLIDiscoveryProvider.discover(spec, self.alternative_executables)
        return exe_path if found else None

    def verify_version(self, executable_path: Path) -> Tuple[bool, Optional[str]]:
        """Execute version command and return (verified, version_string)."""
        return CLIDiscoveryProvider.verify_version(executable_path, self.version_args)

    def find_desktop_application(
        self, search_dirs: Optional[List[Path]] = None
    ) -> Tuple[bool, Optional[Path], Optional[Path], Optional[str]]:
        """Discover desktop application (.desktop launcher, /opt installation, etc.)."""
        spec = self.get_app_spec()
        return DesktopDiscoveryProvider.discover(spec, desktop_search_dirs=search_dirs)

    def find_package_manager_application(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """Discover application installed via package managers (dpkg, rpm, flatpak, snap)."""
        spec = self.get_app_spec()
        return PackageManagerDiscoveryProvider.discover(spec)

    def check_config_present(self) -> bool:
        """Check whether recognized configuration exists for this agent."""
        return False

    def check_skills_dir_present(self, scope: Scope = Scope.GLOBAL, project_root: Optional[Path] = None) -> bool:
        """Check whether native skills directory exists."""
        skill_dir = self.get_skill_dir(scope, project_root)
        return skill_dir.exists() and skill_dir.is_dir()

    def check_project_config_present(self, project_root: Optional[Path] = None) -> bool:
        """Check whether recognized project-level configuration exists."""
        return False

    def detect_status(
        self,
        project_root: Optional[Path] = None,
        desktop_search_dirs: Optional[List[Path]] = None,
    ) -> EnvironmentStatus:
        """Evaluate full multi-method detection status for this environment."""
        if not self.is_application:
            config_present = self.check_config_present()
            skills_dir_present = self.check_skills_dir_present(Scope.GLOBAL)
            proj_config_present = self.check_project_config_present(project_root) if project_root else False
            return EnvironmentStatus(
                adapter_id=self.target_id,
                name=self.name,
                installed=False,
                application_found=False,
                installation_method=InstallationMethod.TARGET_ONLY.value,
                executable_found=False,
                version_verified=False,
                version=None,
                application_path=None,
                executable_path=None,
                config_present=config_present,
                skills_directory_present=skills_dir_present,
                project_config_present=proj_config_present,
                available=True,
                details="Distribution target (not a standalone AI application)",
                global_path=str(self.get_skill_dir(Scope.GLOBAL)),
                project_path=str(self.get_skill_dir(Scope.PROJECT, project_root)),
                detected_system=False,
                detected_project=proj_config_present,
            )

        # 1. CLI Discovery
        exe_path = self.find_executable()
        cli_found = exe_path is not None
        cli_ver_ok = False
        cli_ver = None
        if cli_found and exe_path:
            cli_ver_ok, cli_ver = self.verify_version(exe_path)

        # 2. Desktop Application Discovery
        desktop_found, launcher_path, desktop_bin, desktop_ver = self.find_desktop_application(search_dirs=desktop_search_dirs)

        # 3. Package Manager Discovery
        pkg_found, pkg_manager, pkg_ver = self.find_package_manager_application()

        # Application is verified if desktop app exists, package exists, or CLI is present and version verified
        application_found = bool(desktop_found or pkg_found or (cli_found and cli_ver_ok))

        methods_detected = []
        if desktop_found:
            methods_detected.append("Desktop")
        if cli_found:
            methods_detected.append("CLI")
        if pkg_found and not desktop_found:
            methods_detected.append("Package Manager")

        if desktop_found and cli_found:
            primary_method = "Desktop, CLI"
        elif desktop_found:
            primary_method = "Desktop"
        elif cli_found:
            primary_method = "CLI"
        elif pkg_found:
            primary_method = "Package Manager"
        else:
            primary_method = "—"

        final_ver = cli_ver or desktop_ver or pkg_ver
        version_verified = bool(final_ver is not None)

        app_path = str(desktop_bin) if desktop_bin else (str(exe_path) if exe_path else None)

        config_present = self.check_config_present()
        skills_dir_present = self.check_skills_dir_present(Scope.GLOBAL)
        proj_config_present = self.check_project_config_present(project_root) if project_root else False

        if not application_found:
            if cli_found and not cli_ver_ok:
                details = "Executable found but version verification failed"
            elif config_present and skills_dir_present:
                details = "Configuration and skills directory present without application"
            elif config_present:
                details = "Configuration present without application"
            elif skills_dir_present:
                details = "Skills directory present without application"
            else:
                details = "Executable absent"
        elif desktop_found and cli_found:
            ver_text = f"v{final_ver}" if final_ver else "unknown version"
            details = f"Verified Desktop & CLI installation ({ver_text})"
        elif desktop_found and not cli_found:
            ver_text = f"v{final_ver}" if final_ver else "unknown version"
            details = f"Verified Desktop application ({ver_text}, CLI unavailable)"
        elif cli_found:
            ver_text = f"v{final_ver}" if final_ver else "unknown version"
            details = f"Verified CLI installation ({ver_text})"
        elif pkg_found:
            ver_text = f"v{final_ver}" if final_ver else "unknown version"
            details = f"Verified {pkg_manager} package installation ({ver_text})"
        else:
            details = "Application detected"

        global_dir = self.get_skill_dir(Scope.GLOBAL)
        proj_dir = self.get_skill_dir(Scope.PROJECT, project_root)

        return EnvironmentStatus(
            adapter_id=self.target_id,
            name=self.name,
            installed=application_found,  # verified application installation
            application_found=application_found,
            installation_method=primary_method,
            executable_found=cli_found,
            version_verified=version_verified,
            version=final_ver,
            application_path=app_path,
            executable_path=str(exe_path) if exe_path else None,
            config_present=config_present,
            skills_directory_present=skills_dir_present,
            project_config_present=proj_config_present,
            available=True,
            details=details,
            global_path=str(global_dir),
            project_path=str(proj_dir),
            detected_system=application_found,
            detected_project=proj_config_present,
        )

    def detect(self) -> bool:
        """Detect whether this agent environment is installed."""
        return self.detect_status().installed

    def get_skill_dir(self, scope: Scope, project_root: Optional[Path] = None) -> Path:
        """Resolve the skill directory for the requested scope."""
        if scope == Scope.PROJECT:
            root = project_root or find_project_root()
            if root is None:
                root = Path.cwd().resolve()
            return (root / self.default_project_rel_path).resolve()
        else:
            return (get_user_home() / self.default_global_rel_path).resolve()

    def get_manifest_path(self, scope: Scope, project_root: Optional[Path] = None) -> Path:
        """Return the manifest file path for this target and scope."""
        return self.get_skill_dir(scope, project_root) / MANIFEST_FILE_NAME

    def read_manifest(self, scope: Scope, project_root: Optional[Path] = None) -> TargetManifest:
        """Read and parse the TES manifest in the target directory."""
        mpath = self.get_manifest_path(scope, project_root)
        if not mpath.exists():
            return TargetManifest()
        try:
            content = mpath.read_text(encoding="utf-8")
            return TargetManifest.model_validate_json(content)
        except Exception:
            return TargetManifest()

    def write_manifest(self, manifest: TargetManifest, scope: Scope, project_root: Optional[Path] = None) -> None:
        """Write the updated manifest atomically to the target directory."""
        skill_dir = self.get_skill_dir(scope, project_root)
        skill_dir.mkdir(parents=True, exist_ok=True)
        mpath = skill_dir / MANIFEST_FILE_NAME
        tmp_path = skill_dir / f"{MANIFEST_FILE_NAME}.tmp"
        tmp_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
        tmp_path.replace(mpath)

    def list_installed(self, scope: Scope, project_root: Optional[Path] = None) -> List[InstalledSkillManifest]:
        """List all TES-managed skills recorded in this adapter's manifest."""
        manifest = self.read_manifest(scope, project_root)
        return list(manifest.skills.values())

    def validate_target(self, scope: Scope, project_root: Optional[Path] = None) -> Dict[str, Any]:
        """Verify write access and state of the target directory without mutating disk."""
        skill_dir = self.get_skill_dir(scope, project_root)
        writable = False
        try:
            if skill_dir.exists():
                writable = os.access(skill_dir, os.W_OK)
            else:
                parent = skill_dir.parent
                while not parent.exists() and parent.parent != parent:
                    parent = parent.parent
                writable = os.access(parent, os.W_OK)
        except Exception:
            writable = False

        manifest_exists = (skill_dir / MANIFEST_FILE_NAME).exists()
        managed_count = len(self.read_manifest(scope, project_root).skills)

        return {
            "adapter": self.target_id,
            "name": self.name,
            "scope": scope.value,
            "path": str(skill_dir),
            "exists": skill_dir.exists(),
            "writable": writable,
            "manifest_exists": manifest_exists,
            "managed_skills_count": managed_count,
        }
