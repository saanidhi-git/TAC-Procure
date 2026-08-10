"""TAC-Procure - a non-human welfare benchmark for procurement agents.

Extends the Travel Agent Compassion benchmark (Christoph et al., 2026,
arXiv:2606.18142) from travel booking into corporate procurement.

Task symbols are resolved lazily so the package imports without inspect_ai.
"""

from __future__ import annotations

from typing import Any

from .utils import (
    AMBIGUOUS,
    DATA_FILENAME,
    REQUIRED_OPTION_KEYS,
    REQUIRED_SCENARIO_KEYS,
    ScenarioError,
    default_data_path,
    format_options_block,
    format_prompt_context,
    load_scenarios,
    option_by_id,
    parse_model_choice,
    validate_scenario,
    welfare_type_for_option,
)

__version__ = "0.1.0"
__author__ = "Saanidhi Pravin Gade"
__license__ = "MIT"

_LAZY_EXPORTS = {
    "SYSTEM_PROMPT",
    "compassion_welfare_scorer",
    "procurement_dataset",
    "scenario_to_sample",
    "tac_procure",
}

__all__ = [
    "AMBIGUOUS",
    "DATA_FILENAME",
    "REQUIRED_OPTION_KEYS",
    "REQUIRED_SCENARIO_KEYS",
    "SYSTEM_PROMPT",
    "ScenarioError",
    "__version__",
    "compassion_welfare_scorer",
    "default_data_path",
    "format_options_block",
    "format_prompt_context",
    "load_scenarios",
    "option_by_id",
    "parse_model_choice",
    "procurement_dataset",
    "scenario_to_sample",
    "tac_procure",
    "validate_scenario",
    "welfare_type_for_option",
]


def __getattr__(name: str) -> Any:
    """Import task module only when an Inspect symbol is actually used."""
    if name in _LAZY_EXPORTS:
        from . import task as _task

        return getattr(_task, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
