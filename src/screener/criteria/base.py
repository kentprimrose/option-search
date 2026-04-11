"""
Base classes and registry for option screening criteria.

To add a new criterion:
1. Subclass ``Criterion`` in ``filters.py`` (or any module imported by ``__init__.py``).
2. Decorate the class with ``@register``.
3. Implement ``form_fields()`` and ``apply()``.

The criterion will automatically appear in the UI on next startup.
"""
from abc import ABC, abstractmethod

_registry: dict[str, "Criterion"] = {}


def register(cls: type) -> type:
    """Class decorator that registers a Criterion subclass."""
    instance = cls()
    _registry[instance.id] = instance
    return cls


def get_all_criteria() -> list["Criterion"]:
    return list(_registry.values())


def get_criterion(criterion_id: str) -> "Criterion | None":
    return _registry.get(criterion_id)


class FormField:
    """Describes a single parameter field rendered inside a criterion card."""

    def __init__(
        self,
        name: str,
        label: str,
        field_type: str,
        *,
        default=None,
        min=None,
        max=None,
        step="any",
        choices: list[tuple[str, str]] | None = None,
    ):
        self.name = name
        self.label = label
        self.field_type = field_type  # "number" | "select" | "text"
        self.default = default
        self.min = min
        self.max = max
        self.step = step
        self.choices = choices or []


class Criterion(ABC):
    """Base class for all option screening criteria."""

    id: str
    name: str
    description: str

    @property
    def enable_field_name(self) -> str:
        return f"enable_{self.id}"

    def field_name(self, param: str) -> str:
        return f"{self.id}_{param}"

    def form_fields(self) -> list[FormField]:
        """Return the list of parameter fields shown when this criterion is enabled."""
        return []

    def is_enabled(self, form_data: dict) -> bool:
        return self.enable_field_name in form_data

    @abstractmethod
    def apply(
        self,
        options: list[dict],
        underlying_price: float,
        form_data: dict,
    ) -> list[dict]:
        """Return the subset of *options* that satisfy this criterion."""
