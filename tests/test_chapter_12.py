"""Tests for Chapter 12: Functional Programming."""

import functools
import operator
from typing import Callable


class TestClosures:
    """Test closure patterns."""

    def test_closure_captures_variable(self) -> None:
        """Closures capture variables from the enclosing scope."""

        def make_multiplier(factor: int) -> Callable[[int], int]:
            def multiplier(x: int) -> int:
                return x * factor

            return multiplier

        double = make_multiplier(2)
        triple = make_multiplier(3)

        assert double(5) == 10
        assert triple(5) == 15

    def test_higher_order_function(self) -> None:
        """Functions can accept and return functions."""

        def apply_twice(f: Callable[[int], int], x: int) -> int:
            return f(f(x))

        assert apply_twice(lambda x: x + 3, 10) == 16
        assert apply_twice(lambda x: x * 2, 3) == 12


class TestFunctools:
    """Test functools utilities."""

    def test_partial_binds_arguments(self) -> None:
        """functools.partial pre-fills function arguments."""
        base2_log = functools.partial(int, base=2)
        assert base2_log("1010") == 10
        assert base2_log("1111") == 15

    def test_lru_cache_memoizes(self) -> None:
        """lru_cache caches return values."""
        call_count: int = 0

        @functools.lru_cache(maxsize=None)
        def fibonacci(n: int) -> int:
            nonlocal call_count
            call_count += 1
            if n < 2:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        assert fibonacci(10) == 55
        assert call_count == 11  # Each value computed only once

    def test_reduce_accumulates(self) -> None:
        """functools.reduce applies a function cumulatively."""
        product = functools.reduce(operator.mul, [1, 2, 3, 4, 5])
        assert product == 120

    def test_total_ordering(self) -> None:
        """total_ordering fills in comparison methods."""

        @functools.total_ordering
        class Score:
            def __init__(self, value: int) -> None:
                self.value = value

            def __eq__(self, other: object) -> bool:
                if not isinstance(other, Score):
                    return NotImplemented
                return self.value == other.value

            def __lt__(self, other: "Score") -> bool:
                return self.value < other.value

        assert Score(5) < Score(10)
        assert Score(10) > Score(5)
        assert Score(5) <= Score(5)
        assert Score(10) >= Score(5)


class TestOperatorModule:
    """Test operator module usage."""

    def test_operator_itemgetter(self) -> None:
        """operator.itemgetter for key functions."""
        data = [("Alice", 95), ("Bob", 87), ("Carol", 92)]
        sorted_by_score = sorted(data, key=operator.itemgetter(1))
        assert sorted_by_score[0] == ("Bob", 87)

    def test_operator_attrgetter(self) -> None:
        """operator.attrgetter for attribute access."""

        class Point:
            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y

        points = [Point(3, 1), Point(1, 2), Point(2, 3)]
        sorted_by_x = sorted(points, key=operator.attrgetter("x"))
        assert sorted_by_x[0].x == 1

    def test_operator_functions(self) -> None:
        """operator module provides function equivalents of operators."""
        assert operator.add(2, 3) == 5
        assert operator.mul(4, 5) == 20
        assert operator.neg(-5) == 5
