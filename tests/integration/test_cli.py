"""End-to-end integration tests for the TES CLI commands."""

from pathlib import Path
from typer.testing import CliRunner
from tes.cli import app


def test_cli_version(runner: CliRunner):
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "TES — Techpronnet Engineering Skills" in result.output
    assert "0.2.1" in result.output


def test_cli_search(runner: CliRunner):
    result = runner.invoke(app, ["search", "security"])
    assert result.exit_code == 0
    assert "security-audit" in result.output
    assert "secure-development" in result.output


def test_cli_inspect(runner: CliRunner):
    result = runner.invoke(app, ["inspect", "system-architect"])
    assert result.exit_code == 0
    assert "system-architect" in result.output
    assert "System Architect" in result.output
    assert "Domain modeling" in result.output or "domain" in result.output.lower()


def test_cli_detect(runner: CliRunner):
    result = runner.invoke(app, ["detect"])
    assert result.exit_code == 0
    # Table 1
    assert "Detected AI Coding Environments" in result.output
    assert "Method" in result.output
    assert "CLI" in result.output
    assert "opencode" in result.output
    assert "codex" in result.output
    # Table 2
    assert "Configuration and Skills" in result.output
    assert "TES Support" in result.output


def test_cli_doctor(runner: CliRunner):
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "TES Doctor — Diagnostic Environment" in result.output
    assert "PASS" in result.output


def test_cli_validate(runner: CliRunner):
    result = runner.invoke(app, ["validate"])
    assert result.exit_code == 0
    assert "All 14 skill package(s) passed validation" in result.output


def test_cli_analyze(runner: CliRunner):
    result = runner.invoke(app, ["analyze"])
    assert result.exit_code == 0
    assert "TES Skill Catalogue Analysis" in result.output
    assert "Token Efficiency Summary" in result.output
    assert "14 skills" in result.output


def test_cli_analyze_skill_and_bundle(runner: CliRunner):
    # Single skill
    res_skill = runner.invoke(app, ["analyze", "--skill", "security-audit"])
    assert res_skill.exit_code == 0
    assert "security-audit" in res_skill.output

    # Bundle
    res_bundle = runner.invoke(app, ["analyze", "--bundle", "release-suite"])
    assert res_bundle.exit_code == 0
    assert "devops-engineering" in res_bundle.output
    assert "deployment-verification" in res_bundle.output


def test_cli_analyze_report(runner: CliRunner):
    result = runner.invoke(app, ["analyze", "--report"])
    assert result.exit_code == 0
    assert "# TES Token Efficiency & Skill Diagnostics Report" in result.output
    assert "Skill Sizing & Instruction Budgets" in result.output


def test_cli_install_and_list_and_uninstall(runner: CliRunner, tmp_path: Path, monkeypatch):
    # Set current working directory to isolated temp path
    monkeypatch.chdir(tmp_path)

    # 1. Install
    install_res = runner.invoke(app, ["install", "engineering-core", "--target", "generic", "--scope", "project"])
    assert install_res.exit_code == 0
    assert "Installed engineering-core" in install_res.output

    # 2. List
    list_res = runner.invoke(app, ["list", "--target", "generic", "--scope", "project"])
    assert list_res.exit_code == 0
    assert "engineering-core" in list_res.output

    # 3. Uninstall
    uninstall_res = runner.invoke(app, ["uninstall", "engineering-core", "--target", "generic", "--scope", "project"])
    assert uninstall_res.exit_code == 0
    assert "Successfully uninstalled 'engineering-core'" in uninstall_res.output

    # 4. List again (empty)
    list_after = runner.invoke(app, ["list", "--target", "generic", "--scope", "project"])
    assert list_after.exit_code == 0
    assert "No TES skills currently installed" in list_after.output
