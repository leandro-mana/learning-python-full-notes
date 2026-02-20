"""Tests for Chapter 9: Iterators, Generators, and Comprehensions."""

import itertools
from typing import Generator


class TestIterationProtocol:
    """Test iterator protocol fundamentals."""

    def test_custom_iterator(self) -> None:
        """Custom iterator implements __iter__ and __next__."""

        class Countdown:
            def __init__(self, start: int) -> None:
                self.current = start

            def __iter__(self):
                return self

            def __next__(self) -> int:
                if self.current <= 0:
                    raise StopIteration
                self.current -= 1
                return self.current + 1

        assert list(Countdown(3)) == [3, 2, 1]

    def test_iter_sentinel_form(self) -> None:
        """iter() with sentinel stops at specific value."""
        values = iter([1, 2, 3, 0, 4, 5])
        # Read until we hit 0
        result = list(iter(lambda: next(values), 0))
        assert result == [1, 2, 3]

    def test_iterable_vs_iterator(self) -> None:
        """Iterables create new iterators; iterators are consumed once."""
        data = [1, 2, 3]  # Iterable - can create multiple iterators

        iter1 = iter(data)
        iter2 = iter(data)

        assert next(iter1) == 1
        assert next(iter2) == 1  # Independent iterators

    def test_generator_function(self) -> None:
        """Generator functions yield values lazily."""

        def fibonacci(n: int) -> Generator[int, None, None]:
            a, b = 0, 1
            for _ in range(n):
                yield a
                a, b = b, a + b

        assert list(fibonacci(7)) == [0, 1, 1, 2, 3, 5, 8]


class TestComprehensions:
    """Test advanced comprehension patterns."""

    def test_nested_comprehension(self) -> None:
        """Nested comprehensions for matrix operations."""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        flat = [x for row in matrix for x in row]
        assert flat == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_dict_comprehension_invert(self) -> None:
        """Dict comprehension to invert a mapping."""
        original = {"a": 1, "b": 2, "c": 3}
        inverted = {v: k for k, v in original.items()}
        assert inverted == {1: "a", 2: "b", 3: "c"}

    def test_set_comprehension(self) -> None:
        """Set comprehension for deduplication."""
        words = ["hello", "HELLO", "Hello", "world", "WORLD"]
        unique_lower = {w.lower() for w in words}
        assert unique_lower == {"hello", "world"}

    def test_generator_expression_lazy(self) -> None:
        """Generator expressions are lazy - not computed until consumed."""
        gen = (x**2 for x in range(5))
        assert next(gen) == 0
        assert next(gen) == 1
        assert list(gen) == [4, 9, 16]  # Remaining values

    def test_walrus_in_comprehension(self) -> None:
        """Walrus operator avoids redundant computation."""
        data = ["hello", "hi", "hey", "greetings", "yo"]
        # Compute len once, use twice (filter + transform)
        result = [(word, n) for word in data if (n := len(word)) > 2]
        assert result == [("hello", 5), ("hey", 3), ("greetings", 9)]


class TestItertools:
    """Test itertools patterns."""

    def test_chain(self) -> None:
        """chain combines multiple iterables."""
        result = list(itertools.chain([1, 2], [3, 4], [5]))
        assert result == [1, 2, 3, 4, 5]

    def test_islice(self) -> None:
        """islice for lazy slicing of iterators."""
        result = list(itertools.islice(range(100), 5))
        assert result == [0, 1, 2, 3, 4]

    def test_groupby(self) -> None:
        """groupby groups consecutive elements by key."""
        data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
        groups = {k: list(v) for k, v in itertools.groupby(data, key=lambda x: x[0])}
        assert groups["A"] == [("A", 1), ("A", 2)]
        assert groups["B"] == [("B", 3), ("B", 4)]

    def test_product(self) -> None:
        """product computes cartesian product."""
        result = list(itertools.product("AB", [1, 2]))
        assert result == [("A", 1), ("A", 2), ("B", 1), ("B", 2)]

    def test_accumulate(self) -> None:
        """accumulate produces running totals."""
        result = list(itertools.accumulate([1, 2, 3, 4, 5]))
        assert result == [1, 3, 6, 10, 15]
