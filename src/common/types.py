"""Common type definitions and utilities."""

from typing import Any, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class Result(Generic[T]):
    """Generic result type for error handling."""

    def __init__(self, value: T | None = None, error: str | None = None) -> None:
        self.value = value
        self.error = error

    @property
    def is_ok(self) -> bool:
        """Check if result is successful."""
        return self.error is None

    @property
    def is_err(self) -> bool:
        """Check if result is an error."""
        return self.error is not None

    def unwrap(self) -> T:
        """Unwrap the value, raising if error."""
        if self.is_err:
            raise ValueError(f"Called unwrap on error: {self.error}")
        return self.value  # type: ignore


def ensure_type(value: Any, expected_type: type, name: str = "value") -> None:
    """Ensure a value is of expected type, raise TypeError otherwise."""
    if not isinstance(value, expected_type):
        raise TypeError(f"{name} must be {expected_type.__name__}, " f"got {type(value).__name__}")
