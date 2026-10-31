"""Multi-method AI coding application discovery engine for TES.

Discovers applications through multiple independent installation methods:
- CLI discovery (PATH and known executable locations)
- Desktop application discovery (.desktop launchers, standard /opt or /usr/lib installations)
- Package manager discovery (dpkg/apt, rpm, flatpak, snap)
- Manual installation discovery (known custom application paths)
"""

from dataclasses import dataclass, field
from enum import Enum
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
from typing import Any, Dict, List, Optional, Set, Tuple

from tes.config import get_user_home


class InstallationMethod(str, Enum):
    CLI = "CLI"
    DESKTOP = "Desktop"
    PACKAGE_MANAGER = "Package Manager"
    MANUAL = "Manual"
    DESKTOP_CLI = "Desktop, CLI"
    NONE = "—"
    TARGET_ONLY = "N/A"


@dataclass
class ApplicationSpec:
    """Specification of an AI coding application for discovery."""
    adapter_id: str
    display_name: str
    cli_commands: List[str] = field(default_factory=list)
    cli_version_args: List[str] = field(default_factory=lambda: ["--version"])
    desktop_names: List[str] = field(default_factory=list)
    desktop_file_patterns: List[str] = field(default_factory=list)
    known_app_dirs: List[Path] = field(default_factory=list)
    known_binaries: List[Path] = field(default_factory=list)
    package_names: List[str] = field(default_factory=list)
    flatpak_ids: List[str] = field(default_factory=list)
    snap_names: List[str] = field(default_factory=list)
    version_file_rel_paths: List[str] = field(default_factory=list)
    is_standalone_application: bool = True


@dataclass
class DiscoveryResult:
    """Discovered installation evidence for an application."""
    application_found: bool = False
    installation_method: str = "—"
    installation_methods_detected: List[str] = field(default_factory=list)
    executable_found: bool = False
    executable_path: Optional[str] = None
    application_path: Optional[str] = None
    version_verified: bool = False
    version: Optional[str] = None
    desktop_launcher_path: Optional[str] = None
    package_manager: Optional[str] = None
    details: str = "Not installed"


# Standard Linux desktop entry directories
STANDARD_DESKTOP_DIRS = [
    Path("/usr/share/applications"),
    Path("/usr/local/share/applications"),
    get_user_home() / ".local/share/applications",
    Path("/var/lib/flatpak/exports/share/applications"),
    get_user_home() / ".local/share/flatpak/exports/share/applications",
    Path("/var/lib/snapd/desktop/applications"),
    get_user_home() / ".local/share/snapd/desktop/applications",
]


class CLIDiscoveryProvider:
    """Discovers CLI executables on PATH and known paths with version verification."""

    @classmethod
    def discover(cls, spec: ApplicationSpec, alternative_paths: Optional[List[str]] = None) -> Tuple[bool, Optional[Path], bool, Optional[str]]:
        """Return (executable_found, executable_path, version_verified, version_str)."""
        exe_path: Optional[Path] = None

        # 1. Search PATH for primary CLI commands
        for cmd in spec.cli_commands:
            found = shutil.which(cmd)
            if found:
                exe_path = Path(found).resolve()
                break

        # 2. Search alternative executable paths if not found on PATH
        if not exe_path and alternative_paths:
            home = get_user_home()
            for alt in alternative_paths:
                if "/" in alt:
                    candidate = Path(alt) if Path(alt).is_absolute() else (home / alt)
                    if candidate.exists() and os.access(candidate, os.X_OK):
                        exe_path = candidate.resolve()
                        break
                else:
                    alt_found = shutil.which(alt)
                    if alt_found:
                        exe_path = Path(alt_found).resolve()
                        break

        if not exe_path:
            return False, None, False, None

        # Verify executable version safely
        version_verified, version_str = cls.verify_version(exe_path, spec.cli_version_args)
        return True, exe_path, version_verified, version_str

    @classmethod
    def verify_version(cls, executable_path: Path, version_args: List[str]) -> Tuple[bool, Optional[str]]:
        """Run version command and extract sanitized version string."""
        try:
            res = subprocess.run(
                [str(executable_path)] + version_args,
                capture_output=True,
                text=True,
                timeout=3,
                check=False,
            )
            if res.returncode == 0:
                raw = res.stdout.strip() or res.stderr.strip()
                first_line = raw.splitlines()[0].strip() if raw else ""
                match = re.search(r"(\d+\.\d+(?:\.\d+)?(?:-[a-zA-Z0-9.]+)?|\d+\.\d+)", first_line)
                version_str = match.group(1) if match else (first_line[:30] if first_line else "verified")
                return True, version_str
            return False, None
        except Exception:
            return False, None


class DesktopDiscoveryProvider:
    """Discovers desktop applications from .desktop files, /opt, and standard directories."""

    @classmethod
    def discover(
        cls, spec: ApplicationSpec, desktop_search_dirs: Optional[List[Path]] = None
    ) -> Tuple[bool, Optional[Path], Optional[Path], Optional[str]]:
        """Return (desktop_found, launcher_path, binary_path, version)."""
        search_dirs = desktop_search_dirs if desktop_search_dirs is not None else STANDARD_DESKTOP_DIRS

        # 1. Search .desktop files
        for sdir in search_dirs:
            if not sdir.exists() or not sdir.is_dir():
                continue

            try:
                for entry in sdir.glob("*.desktop"):
                    if not entry.is_file():
                        continue
                    match_found, bin_path, ver = cls._evaluate_desktop_file(entry, spec)
                    if match_found and bin_path:
                        return True, entry, bin_path, ver
            except Exception:
                continue

        # 2. Check known application directories (/opt/AppName, etc.)
        for adir in spec.known_app_dirs:
            if adir.exists() and adir.is_dir():
                # Check for executable inside
                for bin_candidate in spec.known_binaries:
                    if bin_candidate.exists() and os.access(bin_candidate, os.X_OK):
                        ver = cls._extract_dir_version(adir, spec)
                        return True, None, bin_candidate, ver
                # Also check direct child binaries matching spec names
                for cmd in spec.cli_commands + spec.desktop_names:
                    candidate = adir / cmd
                    if candidate.exists() and os.access(candidate, os.X_OK):
                        ver = cls._extract_dir_version(adir, spec)
                        return True, None, candidate, ver

        return False, None, None, None

    @classmethod
    def _evaluate_desktop_file(cls, desktop_file: Path, spec: ApplicationSpec) -> Tuple[bool, Optional[Path], Optional[str]]:
        """Parse and validate a .desktop launcher against spec."""
        filename = desktop_file.name.lower()
        pattern_match = any(
            re.search(pat.replace("*", ".*").lower(), filename) for pat in spec.desktop_file_patterns
        )

        try:
            content = desktop_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return False, None, None

        in_desktop_entry = False
        app_name = ""
        exec_line = ""
        entry_version = ""

        for line in content.splitlines():
            line = line.strip()
            if line == "[Desktop Entry]":
                in_desktop_entry = True
                continue
            if line.startswith("[") and in_desktop_entry:
                break
            if not in_desktop_entry:
                continue

            if line.startswith("Name="):
                app_name = line[5:].strip()
            elif line.startswith("Exec="):
                exec_line = line[5:].strip()
            elif line.startswith("X-AppImage-Version=") or line.startswith("Version="):
                val = line.split("=", 1)[1].strip()
                if re.match(r"^\d+\.\d+", val):
                    entry_version = val

        name_match = any(dname.lower() in app_name.lower() for dname in spec.desktop_names)
        if not (name_match or pattern_match):
            return False, None, None

        if not exec_line:
            return False, None, None

        # Validate that the binary target in Exec actually exists on disk
        target_bin = cls._resolve_exec_target(exec_line)
        if not target_bin:
            return False, None, None

        # Extract version from file if possible, or from version file
        extracted_ver = entry_version or cls._extract_app_version(target_bin, spec)
        return True, target_bin, extracted_ver

    @classmethod
    def _resolve_exec_target(cls, exec_line: str) -> Optional[Path]:
        """Extract and validate the binary path from an Exec= line."""
        try:
            parts = shlex.split(exec_line)
        except Exception:
            parts = exec_line.split()

        if not parts:
            return None

        raw_cmd = parts[0]
        # Ignore desktop field codes if accidentally parsed as command
        if raw_cmd.startswith("%"):
            return None

        # Absolute or relative path
        if "/" in raw_cmd:
            candidate = Path(raw_cmd)
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return candidate.resolve()
            return None

        # Command name on PATH
        found = shutil.which(raw_cmd)
        if found:
            return Path(found).resolve()

        return None

    @classmethod
    def _extract_dir_version(cls, app_dir: Path, spec: ApplicationSpec) -> Optional[str]:
        """Extract version from known relative paths inside the application directory."""
        for rel_path in spec.version_file_rel_paths:
            vfile = app_dir / rel_path
            if vfile.exists() and vfile.is_file():
                try:
                    raw = vfile.read_text(encoding="utf-8", errors="ignore").strip()
                    match = re.search(r"(\d+\.\d+(?:\.\d+)?)", raw)
                    if match:
                        return match.group(1)
                except Exception:
                    pass
        return None

    @classmethod
    def _extract_app_version(cls, bin_path: Path, spec: ApplicationSpec) -> Optional[str]:
        """Attempt to read version metadata from parent directories of the binary."""
        current = bin_path.parent
        for _ in range(3):
            ver = cls._extract_dir_version(current, spec)
            if ver:
                return ver
            if current.parent == current:
                break
            current = current.parent
        return None


class PackageManagerDiscoveryProvider:
    """Discovers applications registered via dpkg/apt, rpm, flatpak, or snap."""

    @classmethod
    def discover(cls, spec: ApplicationSpec) -> Tuple[bool, Optional[str], Optional[str]]:
        """Return (package_installed, manager_name, version)."""
        # 1. dpkg (Debian / Ubuntu / Kali)
        if shutil.which("dpkg"):
            for pkg in spec.package_names:
                try:
                    res = subprocess.run(
                        ["dpkg", "-s", pkg],
                        capture_output=True,
                        text=True,
                        timeout=2,
                        check=False,
                    )
                    if res.returncode == 0 and "Status: install ok installed" in res.stdout:
                        ver_match = re.search(r"Version:\s*([^\s]+)", res.stdout)
                        pkg_ver = ver_match.group(1) if ver_match else None
                        return True, "dpkg", pkg_ver
                except Exception:
                    pass

        # 2. rpm (RedHat / Fedora / openSUSE)
        if shutil.which("rpm"):
            for pkg in spec.package_names:
                try:
                    res = subprocess.run(
                        ["rpm", "-q", "--qf", "%{VERSION}", pkg],
                        capture_output=True,
                        text=True,
                        timeout=2,
                        check=False,
                    )
                    if res.returncode == 0 and res.stdout.strip() and "not installed" not in res.stdout:
                        return True, "rpm", res.stdout.strip()
                except Exception:
                    pass

        # 3. Flatpak
        if shutil.which("flatpak"):
            for f_id in spec.flatpak_ids:
                try:
                    res = subprocess.run(
                        ["flatpak", "info", f_id],
                        capture_output=True,
                        text=True,
                        timeout=2,
                        check=False,
                    )
                    if res.returncode == 0:
                        ver_match = re.search(r"Version:\s*([^\s]+)", res.stdout)
                        f_ver = ver_match.group(1) if ver_match else None
                        return True, "flatpak", f_ver
                except Exception:
                    pass

        # 4. Snap
        if shutil.which("snap"):
            for s_name in spec.snap_names:
                try:
                    res = subprocess.run(
                        ["snap", "list", s_name],
                        capture_output=True,
                        text=True,
                        timeout=2,
                        check=False,
                    )
                    if res.returncode == 0:
                        lines = [l for l in res.stdout.splitlines() if l.strip() and not l.startswith("Name")]
                        if lines:
                            parts = lines[0].split()
                            s_ver = parts[1] if len(parts) > 1 else None
                            return True, "snap", s_ver
                except Exception:
                    pass

        return False, None, None


class ApplicationDiscoveryEngine:
    """Orchestrates multi-method application discovery across CLI, Desktop, and Package Managers."""

    def __init__(
        self,
        desktop_dirs: Optional[List[Path]] = None,
    ):
        self.desktop_dirs = desktop_dirs

    def discover(self, spec: ApplicationSpec, alternative_cli_paths: Optional[List[str]] = None) -> DiscoveryResult:
        """Evaluate all discovery methods independently and synthesize evidence."""
        if not spec.is_standalone_application:
            return DiscoveryResult(
                application_found=False,
                installation_method=InstallationMethod.TARGET_ONLY.value,
                installation_methods_detected=[],
                executable_found=False,
                version_verified=False,
                version=None,
                details="Distribution target (not a standalone AI application)",
            )

        # 1. CLI Discovery
        cli_found, cli_path, cli_ver_ok, cli_ver = CLIDiscoveryProvider.discover(
            spec, alternative_paths=alternative_cli_paths
        )

        # 2. Desktop Application Discovery
        desktop_found, launcher_path, desktop_bin, desktop_ver = DesktopDiscoveryProvider.discover(
            spec, desktop_search_dirs=self.desktop_dirs
        )

        # 3. Package Manager Discovery
        pkg_found, pkg_manager, pkg_ver = PackageManagerDiscoveryProvider.discover(spec)

        # Synthesize evidence
        methods_detected: List[str] = []
        if desktop_found:
            methods_detected.append(InstallationMethod.DESKTOP.value)
        if cli_found:
            methods_detected.append(InstallationMethod.CLI.value)
        if pkg_found and not desktop_found:
            methods_detected.append(InstallationMethod.PACKAGE_MANAGER.value)

        application_found = bool(cli_found or desktop_found or pkg_found)

        # Determine primary installation method label
        if desktop_found and cli_found:
            primary_method = InstallationMethod.DESKTOP_CLI.value
        elif desktop_found:
            primary_method = InstallationMethod.DESKTOP.value
        elif cli_found:
            primary_method = InstallationMethod.CLI.value
        elif pkg_found:
            primary_method = InstallationMethod.PACKAGE_MANAGER.value
        else:
            primary_method = InstallationMethod.NONE.value

        # Determine best application version
        final_ver = cli_ver or desktop_ver or pkg_ver
        version_verified = bool(final_ver is not None)

        # Determine verified application path
        app_path = str(desktop_bin) if desktop_bin else (str(cli_path) if cli_path else None)

        # Build descriptive details string
        if not application_found:
            details = "Executable absent, no desktop application or package detected"
        elif desktop_found and cli_found:
            ver_text = f"v{final_ver}" if final_ver else "unknown version"
            details = f"Verified Desktop & CLI installation ({ver_text})"
        elif desktop_found and not cli_found:
            ver_text = f"v{final_ver}" if final_ver else "unknown version"
            details = f"Verified Desktop application ({ver_text}, CLI unavailable)"
        elif cli_found and not desktop_found:
            ver_text = f"v{final_ver}" if final_ver else "unknown version"
            details = f"Verified CLI executable ({ver_text})"
        elif pkg_found:
            ver_text = f"v{final_ver}" if final_ver else "unknown version"
            details = f"Verified {pkg_manager} package installation ({ver_text})"
        else:
            details = "Application detected"

        return DiscoveryResult(
            application_found=application_found,
            installation_method=primary_method,
            installation_methods_detected=methods_detected,
            executable_found=cli_found,
            executable_path=str(cli_path) if cli_path else None,
            application_path=app_path,
            version_verified=version_verified,
            version=final_ver,
            desktop_launcher_path=str(launcher_path) if launcher_path else None,
            package_manager=pkg_manager,
            details=details,
        )
