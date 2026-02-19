"""Tests for Chapter 6: Exceptions and Error Handling."""

import warnings

import pytest


class TestExceptionBasics:
    """Test exception handling fundamentals."""

    def test_try_except_catches_specific(self) -> None:
        """try/except catches specific exception types."""
        with pytest.raises(ZeroDivisionError):
            1 / 0

    def test_else_runs_on_success(self) -> None:
        """else clause only runs when no exception is raised."""
        ran_else = False
        try:
            result = 10 / 2
        except ZeroDivisionError:
            pass
        else:
            ran_else = True
        assert ran_else
        assert result == 5.0

    def test_finally_always_runs(self) -> None:
        """finally clause runs regardless of exception."""
        cleanup_ran = False
        try:
            raise ValueError("test")
        except ValueError:
            pass
        finally:
            cleanup_ran = True
        assert cleanup_ran

    def test_exception_hierarchy(self) -> None:
        """Exceptions follow class hierarchy for catching."""
        with pytest.raises(LookupError):
            raise KeyError("test")  # KeyError is a LookupError

        with pytest.raises(ArithmeticError):
            raise ZeroDivisionError()  # ZeroDivisionError is ArithmeticError


class TestCustomExceptions:
    """Test custom exception patterns."""

    def test_custom_exception_with_attributes(self) -> None:
        """Custom exceptions can carry structured data."""

        class ValidationError(Exception):
            def __init__(self, field: str, message: str) -> None:
                self.field = field
                self.message = message
                super().__init__(f"{field}: {message}")

        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("email", "invalid format")

        assert exc_info.value.field == "email"
        assert exc_info.value.message == "invalid format"
        assert "email: invalid format" in str(exc_info.value)

    def test_exception_chaining_from(self) -> None:
        """raise ... from preserves the original cause."""

        class AppError(Exception):
            pass

        with pytest.raises(AppError) as exc_info:
            try:
                int("not_a_number")
            except ValueError as e:
                raise AppError("Parse failed") from e

        assert isinstance(exc_info.value.__cause__, ValueError)

    def test_exception_chaining_suppressed(self) -> None:
        """raise ... from None suppresses the context."""

        class NotFoundError(Exception):
            pass

        with pytest.raises(NotFoundError) as exc_info:
            try:
                {"a": 1}["b"]
            except KeyError:
                raise NotFoundError("item not found") from None

        assert exc_info.value.__cause__ is None
        assert exc_info.value.__suppress_context__ is True


class TestExceptionPatterns:
    """Test production exception patterns."""

    def test_eafp_pattern(self) -> None:
        """EAFP is preferred over LBYL in Python."""
        config: dict[str, str] = {"port": "8080"}

        # EAFP style
        try:
            port = int(config["port"])
        except (KeyError, ValueError):
            port = 80

        assert port == 8080

        # Missing key falls back
        try:
            port = int({}["port"])
        except (KeyError, ValueError):
            port = 80

        assert port == 80

    def test_exception_group(self) -> None:
        """ExceptionGroup collects multiple errors."""
        errors = [ValueError("bad value"), TypeError("bad type")]
        group = ExceptionGroup("multiple errors", errors)

        assert len(group.exceptions) == 2
        assert isinstance(group.exceptions[0], ValueError)
        assert isinstance(group.exceptions[1], TypeError)

    def test_warnings_non_fatal(self) -> None:
        """Warnings signal issues without stopping execution."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            warnings.warn("deprecated feature", DeprecationWarning)

        assert len(caught) == 1
        assert issubclass(caught[0].category, DeprecationWarning)
