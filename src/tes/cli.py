"""Command-line interface for TES using Typer and Rich."""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from tes import __version__
from tes.adapters import detect_active_adapters, get_adapter, get_all_adapters, get_default_adapter
from tes.config import find_project_root, get_skills_source_dir
from tes.detector import Detector
from tes.doctor import Doctor
from tes.installer import Installer, SkillConflictError
from tes.models import Scope
from tes.registry import Registry
from tes.uninstaller import Uninstaller, UnmanagedSkillError
from tes.updater import Updater
from tes.validator import SkillValidator

app = typer.Typer(
    name="tes",
    help="TES: Techpronnet Engineering Skills CLI. Manage and distribute reusable AI engineering skills across coding agents.",
    add_completion=False,
    no_args_is_help=True
)
console = Console()


@app.command()
def version():
    """Display TES CLI version and runtime information."""
    console.print(
        Panel(
            f"[bold cyan]TES — Techpronnet Engineering Skills[/bold cyan]\n"
            f"[white]Version:[/white] [green]{__version__}[/green]\n"
            f"[white]Organization:[/white] Techpronnet Technologies\n"
            f"[white]Standard:[/white] Open Agent Skills (agentskills.io)",
            title="TES Version Info",
            box=box.ROUNDED,
        )
    )


@app.command()
def search(
    query: str = typer.Argument("", help="Search keyword (name, description, or tag)"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category (engineering, security, devops, design, memory)"),
):
    """Search available skills in the TES registry."""
    reg = Registry()
    try:
        reg.load()
    except Exception as e:
        console.print(f"[bold red]Error loading registry:[/bold red] {e}")
        raise typer.Exit(1)

    results = reg.search_skills(query, category=category)
    if not results:
        console.print(f"[yellow]No skills found matching '{query}'.[/yellow]")
        return

    table = Table(title=f"TES Skills Catalogue ({len(results)} found)", box=box.ROUNDED)
    table.add_column("Skill ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="bold white")
    table.add_column("Category", style="magenta")
    table.add_column("Version", style="green")
    table.add_column("Description", style="white")

    for s in results:
        desc = (s.description[:75] + "...") if len(s.description) > 78 else s.description
        table.add_row(s.id, s.name, s.category, s.version, desc)

    console.print(table)


@app.command()
def inspect(
    skill_id: str = typer.Argument(..., help="Skill identifier to inspect (e.g. engineering-core)")
):
    """Inspect metadata, principles, and bundled assets of a skill."""
    reg = Registry()
    reg.load()
    skill = reg.get_skill(skill_id)

    if not skill:
        console.print(f"[bold red]Skill '{skill_id}' not found in registry.[/bold red]")
        raise typer.Exit(1)

    source_path = reg.get_skill_source_path(skill)
    tags_str = ", ".join(skill.tags) if skill.tags else "None"
    compat_str = ", ".join(skill.compatibility) if skill.compatibility else "All"

    content = (
        f"[bold cyan]ID:[/bold cyan] {skill.id}\n"
        f"[bold cyan]Name:[/bold cyan] {skill.name}\n"
        f"[bold cyan]Version:[/bold cyan] {skill.version}\n"
        f"[bold cyan]Category:[/bold cyan] {skill.category}\n"
        f"[bold cyan]Tags:[/bold cyan] {tags_str}\n"
        f"[bold cyan]Compatibility:[/bold cyan] {compat_str}\n"
        f"[bold cyan]Source Path:[/bold cyan] {source_path}\n\n"
        f"[bold white]Description:[/bold white]\n{skill.description}"
    )

    console.print(Panel(content, title=f"Skill Inspection: {skill.id}", box=box.ROUNDED))

    # Inspect on-disk assets
    if source_path.exists():
        table = Table(title="Bundled Assets & References", box=box.SIMPLE)
        table.add_column("Relative Path", style="cyan")
        table.add_column("Type", style="green")

        for p in sorted(source_path.rglob("*")):
            if p.is_file():
                rel = p.relative_to(source_path)
                table.add_row(str(rel), "Asset / Reference")
        console.print(table)


@app.command()
def detect():
    """Detect available AI coding environments and active skill directories."""
    report = Detector.detect_environments()

    table = Table(title="Detected AI Coding Environments", box=box.ROUNDED)
    table.add_column("Adapter", style="cyan")
    table.add_column("Environment", style="bold white")
    table.add_column("System Detected", style="green")
    table.add_column("Project Config", style="yellow")
    table.add_column("Global Target Path", style="dim")

    for env in report.detected_environments:
        sys_mark = "[green]✓ Yes[/green]" if env.detected_system else "[dim]No[/dim]"
        proj_mark = "[green]✓ Yes[/green]" if env.detected_project else "[dim]No[/dim]"
        table.add_row(env.adapter_id, env.name, sys_mark, proj_mark, env.global_path)

    console.print(table)
    console.print(f"[bold]Current Project Root:[/bold] {report.project_root}")
    console.print(f"[bold]Recommended Default Target:[/bold] [green]{report.primary_recommended}[/green]\n")


@app.command()
def install(
    target_identifier: str = typer.Argument(..., help="Skill ID (e.g. engineering-core) or Bundle ID (e.g. complete-suite)"),
    target: Optional[str] = typer.Option(None, "--target", "-t", help="Target AI agent (hermes, opencode, codex, claude-code, gemini-cli, generic)"),
    scope: str = typer.Option("project", "--scope", "-s", help="Installation scope: 'project' or 'global'"),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite if destination already exists"),
):
    """Install a skill or bundle into a target AI coding environment."""
    scope_enum = Scope.GLOBAL if scope.lower() == "global" else Scope.PROJECT

    # Determine adapter
    if target:
        try:
            adapter = get_adapter(target)
        except KeyError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(1)
    else:
        adapter = get_default_adapter()
        console.print(f"[dim]No target specified. Auto-selected target adapter: [bold cyan]{adapter.name}[/bold cyan][/dim]")

    reg = Registry()
    reg.load()

    try:
        skills_to_install, bundle_id = reg.resolve_skills_to_install(target_identifier)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

    installer = Installer(adapter, scope=scope_enum)
    skills_with_paths = [(s, reg.get_skill_source_path(s)) for s in skills_to_install]

    if bundle_id:
        console.print(f"Installing bundle [bold cyan]{bundle_id}[/bold cyan] ({len(skills_to_install)} skills) into [green]{adapter.name}[/green] ({scope_enum.value} scope)...")
    else:
        console.print(f"Installing skill [bold cyan]{target_identifier}[/bold cyan] into [green]{adapter.name}[/green] ({scope_enum.value} scope)...")

    try:
        records = installer.install_multiple(skills_with_paths, force=force)
        for r in records:
            console.print(f"  [green]✓ Installed[/green] [bold]{r.skill_id}[/bold] (v{r.version}) -> {adapter.get_skill_dir(scope_enum) / r.skill_id}")
        console.print(f"\n[bold green]Success:[/bold green] All {len(records)} skills installed and recorded in manifest.")
    except SkillConflictError as e:
        console.print(f"\n[bold red]Installation Conflict:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Installation Failed:[/bold red] {e}")
        raise typer.Exit(1)


@app.command("list")
def list_installed(
    target: Optional[str] = typer.Option(None, "--target", "-t", help="Target AI agent (hermes, opencode, codex, claude-code, gemini-cli, generic)"),
    scope: str = typer.Option("project", "--scope", "-s", help="Scope: 'project' or 'global'"),
):
    """List TES-managed skills currently installed."""
    scope_enum = Scope.GLOBAL if scope.lower() == "global" else Scope.PROJECT

    if target:
        try:
            adapters = [get_adapter(target)]
        except KeyError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(1)
    else:
        adapters = get_all_adapters()

    total_found = 0
    table = Table(title=f"Installed TES Skills ({scope_enum.value} scope)", box=box.ROUNDED)
    table.add_column("Target Agent", style="cyan")
    table.add_column("Skill ID", style="bold white", no_wrap=True)
    table.add_column("Version", style="green")
    table.add_column("Installed At", style="yellow")
    table.add_column("Files Managed", style="dim")

    for adapter in adapters:
        skills = adapter.list_installed(scope_enum)
        for s in skills:
            total_found += 1
            table.add_row(adapter.name, s.skill_id, s.version, s.installed_at[:19], str(len(s.managed_files)))

    if total_found == 0:
        console.print(f"[yellow]No TES skills currently installed in {scope_enum.value} scope.[/yellow]")
    else:
        console.print(table)


@app.command()
def update(
    skill_id: Optional[str] = typer.Argument(None, help="Specific skill ID to update, or omit to check all installed skills"),
    target: Optional[str] = typer.Option(None, "--target", "-t", help="Target AI agent"),
    scope: str = typer.Option("project", "--scope", "-s", help="Scope: 'project' or 'global'"),
    preview: bool = typer.Option(False, "--preview", "-p", help="Preview updates without applying modifications"),
):
    """Check for and safely apply updates to installed skills."""
    scope_enum = Scope.GLOBAL if scope.lower() == "global" else Scope.PROJECT
    adapter = get_adapter(target) if target else get_default_adapter()

    reg = Registry()
    reg.load()

    updater = Updater(adapter, reg, scope=scope_enum)
    statuses = updater.check_updates(skill_id)

    if not statuses:
        console.print("[yellow]No installed skills found to check for updates.[/yellow]")
        return

    table = Table(title=f"Skill Update Status ({adapter.name})", box=box.ROUNDED)
    table.add_column("Skill ID", style="cyan")
    table.add_column("Installed Version", style="white")
    table.add_column("Latest Version", style="green")
    table.add_column("Status", style="bold")

    for s in statuses:
        status_text = "[green]Update Available[/green]" if s.update_available else "[dim]Up to date[/dim]"
        table.add_row(s.skill_id, s.installed_version, s.latest_version, status_text)

    console.print(table)

    if preview:
        console.print("\n[dim]Preview mode enabled: No changes applied.[/dim]")
        return

    # Apply updates for available
    updated_count = 0
    for s in statuses:
        if s.update_available:
            res = updater.update_skill(s.skill_id)
            console.print(f"  [green]✓ Updated[/green] {s.skill_id} from v{res['previous_version']} to v{res['new_version']}")
            updated_count += 1

    if updated_count > 0:
        console.print(f"\n[bold green]Success:[/bold green] Updated {updated_count} skills.")
    else:
        console.print("\nAll installed skills are already up to date.")


@app.command()
def uninstall(
    skill_id: str = typer.Argument(..., help="Skill ID to safely remove"),
    target: Optional[str] = typer.Option(None, "--target", "-t", help="Target AI agent"),
    scope: str = typer.Option("project", "--scope", "-s", help="Scope: 'project' or 'global'"),
):
    """Safely uninstall a TES-managed skill."""
    scope_enum = Scope.GLOBAL if scope.lower() == "global" else Scope.PROJECT
    adapter = get_adapter(target) if target else get_default_adapter()

    uninstaller = Uninstaller(adapter, scope=scope_enum)

    try:
        removed = uninstaller.uninstall_skill(skill_id)
        if removed:
            console.print(f"[bold green]Successfully uninstalled '{skill_id}' from {adapter.name} ({scope_enum.value} scope).[/bold green]")
        else:
            console.print(f"[yellow]Skill '{skill_id}' was not found in {adapter.name} manifest.[/yellow]")
    except UnmanagedSkillError as e:
        console.print(f"[bold red]Safety Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Uninstall failed:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def doctor():
    """Diagnose local environment, write permissions, and manifest integrity."""
    report = Doctor.run_diagnostics()

    console.print(Panel(
        f"[bold white]Platform:[/bold white] {report.platform_info}\n"
        f"[bold white]Python:[/bold white] {report.python_version} ({report.python_executable})\n"
        f"[bold white]Project Root:[/bold white] {report.project_root}",
        title="TES Doctor — Diagnostic Environment",
        box=box.ROUNDED
    ))

    table = Table(title="Diagnostic Checks", box=box.ROUNDED)
    table.add_column("Category", style="cyan")
    table.add_column("Check", style="bold white")
    table.add_column("Status", style="bold")
    table.add_column("Details", style="white")

    for c in report.checks:
        status_str = "[green]PASS[/green]" if c.passed else "[red]FAIL[/red]"
        table.add_row(c.category, c.name, status_str, c.details)

    console.print(table)

    if report.all_healthy:
        console.print("\n[bold green]✓ All diagnostic checks passed. System is fully operational.[/bold green]\n")
    else:
        console.print(f"\n[bold red]Found {report.issues_count} diagnostic issue(s):[/bold red]")
        for c in report.checks:
            if not c.passed and c.recommendation:
                console.print(f"  • [yellow]{c.name}:[/yellow] {c.recommendation}")
        console.print()


@app.command()
def validate(
    target_path: Optional[str] = typer.Argument(None, help="Path to specific skill directory or all skills if omitted")
):
    """Validate skill packages for open Agent Skills compliance and integrity."""
    skills_dir = Path(target_path) if target_path else get_skills_source_dir()

    if not skills_dir.exists():
        console.print(f"[bold red]Path not found:[/bold red] {skills_dir}")
        raise typer.Exit(1)

    skill_dirs = [skills_dir] if (skills_dir / "SKILL.md").exists() else [p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]

    table = Table(title="Skill Validation Results", box=box.ROUNDED)
    table.add_column("Skill ID", style="cyan")
    table.add_column("Valid", style="bold")
    table.add_column("Issues / Warnings", style="white")

    all_valid = True
    for sdir in sorted(skill_dirs, key=lambda p: p.name):
        res = SkillValidator.validate_skill_dir(sdir)
        if not res.valid:
            all_valid = False
            status_text = "[red]FAIL[/red]"
            notes = "; ".join(res.errors)
        else:
            status_text = "[green]PASS[/green]"
            notes = "; ".join(res.warnings) if res.warnings else "[dim]None[/dim]"

        table.add_row(res.skill_id, status_text, notes)

    console.print(table)

    if all_valid:
        console.print(f"\n[bold green]✓ All {len(skill_dirs)} skill package(s) passed validation.[/bold green]\n")
    else:
        console.print("\n[bold red]Validation failures detected. Please review errors above.[/bold red]\n")
        raise typer.Exit(1)
