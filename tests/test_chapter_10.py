"""Tests for Chapter 10: Concurrency, Testing, and Best Practices."""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from unittest.mock import MagicMock, patch


class TestConcurrency:
    """Test concurrency patterns."""

    def test_thread_pool_executor(self) -> None:
        """ThreadPoolExecutor runs tasks concurrently."""
        results: list[int] = []

        def square(n: int) -> int:
            return n**2

        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(square, i) for i in range(5)]
            for future in as_completed(futures):
                results.append(future.result())

        assert sorted(results) == [0, 1, 4, 9, 16]

    def test_thread_safe_with_lock(self) -> None:
        """Lock prevents race conditions."""
        counter = {"value": 0}
        lock = Lock()

        def increment(n: int) -> None:
            for _ in range(n):
                with lock:
                    counter["value"] += 1

        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(increment, 100) for _ in range(4)]
            for f in futures:
                f.result()

        assert counter["value"] == 400

    def test_future_exception_handling(self) -> None:
        """Futures propagate exceptions on result()."""

        def failing_task() -> None:
            raise ValueError("task failed")

        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(failing_task)
            exc = future.exception()

        assert isinstance(exc, ValueError)
        assert "task failed" in str(exc)


class TestTestingPatterns:
    """Test testing patterns (meta!)."""

    def test_mock_basic(self) -> None:
        """MagicMock replaces objects for testing."""
        mock_db = MagicMock()
        mock_db.query.return_value = [{"id": 1, "name": "Alice"}]

        result = mock_db.query("SELECT * FROM users")
        assert result == [{"id": 1, "name": "Alice"}]
        mock_db.query.assert_called_once_with("SELECT * FROM users")

    def test_mock_side_effect(self) -> None:
        """side_effect controls mock behavior per call."""
        mock_api = MagicMock()
        mock_api.fetch.side_effect = [ConnectionError("timeout"), {"data": "ok"}]

        # First call raises
        try:
            mock_api.fetch()
            raised = False
        except ConnectionError:
            raised = True
        assert raised

        # Second call succeeds
        result = mock_api.fetch()
        assert result == {"data": "ok"}

    def test_patch_decorator(self) -> None:
        """@patch replaces objects during test."""
        with patch("time.time", return_value=1000.0):
            assert time.time() == 1000.0


class TestDebuggingAndProfiling:
    """Test debugging and performance patterns."""

    def test_assert_for_invariants(self) -> None:
        """assert validates assumptions during development."""

        def process(items: list[int]) -> float:
            assert len(items) > 0, "items must not be empty"
            return sum(items) / len(items)

        assert process([1, 2, 3]) == 2.0

        try:
            process([])
            failed = False
        except AssertionError as e:
            failed = True
            assert "items must not be empty" in str(e)
        assert failed

    def test_logging_levels(self) -> None:
        """Logging module supports multiple severity levels."""
        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.DEBUG)

        _ = (
            logging.handlers.MemoryHandler(capacity=100)
            if hasattr(logging, "handlers")
            else logging.StreamHandler()
        )

        assert logging.DEBUG < logging.INFO < logging.WARNING < logging.ERROR < logging.CRITICAL

    def test_timeit_measurement(self) -> None:
        """timeit measures execution time."""
        import timeit

        # Measure a simple operation
        elapsed = timeit.timeit("sum(range(100))", number=1000)
        assert elapsed > 0  # Just verify it ran and returned a positive time

    def test_sys_getsizeof(self) -> None:
        """sys.getsizeof reports object memory usage."""
        import sys

        list_size = sys.getsizeof([1, 2, 3])
        tuple_size = sys.getsizeof((1, 2, 3))

        # Both should report positive sizes
        assert list_size > 0
        assert tuple_size > 0
        # Tuples are typically smaller than lists
        assert tuple_size <= list_size
