"""Tests for Chapter 21: Logging and Debugging."""

import logging
import traceback


class TestLoggingFundamentals:
    """Test logging module basics."""

    def test_log_levels_ordering(self) -> None:
        """Log levels have a numeric ordering."""
        assert logging.DEBUG < logging.INFO
        assert logging.INFO < logging.WARNING
        assert logging.WARNING < logging.ERROR
        assert logging.ERROR < logging.CRITICAL

    def test_logger_creation(self) -> None:
        """getLogger returns a named logger."""
        logger = logging.getLogger("test.module")
        assert logger.name == "test.module"
        assert isinstance(logger, logging.Logger)

    def test_handler_and_formatter(self) -> None:
        """Handlers format and route log records."""
        logger = logging.getLogger("test.handler")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
        handler.setFormatter(formatter)

        record = logger.makeRecord("test.handler", logging.INFO, "", 0, "hello", (), None)
        formatted = handler.format(record)
        assert "INFO" in formatted
        assert "hello" in formatted

    def test_logger_hierarchy(self) -> None:
        """Child loggers inherit from parent loggers."""
        parent = logging.getLogger("myapp")
        child = logging.getLogger("myapp.module")
        assert child.parent is parent


class TestDebugging:
    """Test debugging utilities."""

    def test_traceback_format(self) -> None:
        """traceback module formats exception information."""
        try:
            raise ValueError("test error")
        except ValueError:
            tb = traceback.format_exc()
            assert "ValueError" in tb
            assert "test error" in tb

    def test_traceback_extract(self) -> None:
        """traceback.extract_stack captures the call stack."""
        stack = traceback.extract_stack()
        assert len(stack) > 0
        # Last frame is this function
        assert "test_traceback_extract" in stack[-1].name

    def test_breakpoint_function_exists(self) -> None:
        """breakpoint() is a built-in function."""
        assert callable(breakpoint)

    def test_exception_chaining(self) -> None:
        """Exception chaining preserves the original cause."""
        try:
            try:
                raise KeyError("original")
            except KeyError as e:
                raise ValueError("wrapper") from e
        except ValueError as e:
            assert isinstance(e.__cause__, KeyError)
            assert str(e.__cause__) == "'original'"
