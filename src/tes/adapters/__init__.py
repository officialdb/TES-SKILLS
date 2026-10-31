"""Adapter registry and discovery for supported AI coding environments."""

from typing import Dict, List, Optional
from tes.adapters.base import BaseAdapter
from tes.adapters.hermes import HermesAdapter
from tes.adapters.opencode import OpenCodeAdapter
from tes.adapters.codex import CodexAdapter
from tes.adapters.claude_code import ClaudeCodeAdapter
from tes.adapters.gemini_cli import GeminiCliAdapter
from tes.adapters.generic import GenericAdapter

_ADAPTERS: Dict[str, BaseAdapter] = {
    "hermes": HermesAdapter(),
    "opencode": OpenCodeAdapter(),
    "codex": CodexAdapter(),
    "claude-code": ClaudeCodeAdapter(),
    "gemini-cli": GeminiCliAdapter(),
    "generic": GenericAdapter(),
}


def get_adapter(target_id: str) -> BaseAdapter:
    """Retrieve an adapter by its target ID.
    
    Raises:
        KeyError: If target_id is unrecognized.
    """
    normalized = target_id.lower().strip()
    if normalized in _ADAPTERS:
        return _ADAPTERS[normalized]
    
    # Handle slight variations
    alias_map = {
        "claude": "claude-code",
        "gemini": "gemini-cli",
        "agent": "generic",
        "agents": "generic",
    }
    if normalized in alias_map:
        return _ADAPTERS[alias_map[normalized]]

    valid = ", ".join(_ADAPTERS.keys())
    raise KeyError(f"Unknown adapter target '{target_id}'. Supported targets: {valid}")


def get_all_adapters() -> List[BaseAdapter]:
    """Return all available adapters."""
    return list(_ADAPTERS.values())


def detect_active_adapters() -> List[BaseAdapter]:
    """Detect which adapters have active environments on the current host."""
    detected = []
    for adapter in _ADAPTERS.values():
        if adapter.detect():
            detected.append(adapter)
    return detected


def get_default_adapter() -> BaseAdapter:
    """Return the preferred active adapter, or fallback to Generic."""
    active = detect_active_adapters()
    if active:
        # If generic is not the only one, return the first specialized active adapter
        specialized = [a for a in active if a.target_id != "generic"]
        if specialized:
            return specialized[0]
        return active[0]
    return _ADAPTERS["generic"]
