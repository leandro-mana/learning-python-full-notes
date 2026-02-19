"""Tests for Chapter 1: Getting Started - Python Fundamentals."""

import pytest


class TestDataTypesAndMutability:
    """Test core data type concepts from Chapter 1."""

    def test_immutable_types_identity(self) -> None:
        """Immutable types with same value may share identity (interning)."""
        a: int = 42
        b: int = 42
        assert a == b
        assert isinstance(a, int)

    def test_mutable_types_independence(self) -> None:
        """Mutable types are independent objects even with same content."""
        list_a: list[int] = [1, 2, 3]
        list_b: list[int] = [1, 2, 3]
        assert list_a == list_b
        assert list_a is not list_b

    def test_tuple_immutability(self) -> None:
        """Tuples cannot be modified after creation."""
        coords: tuple[int, int] = (10, 20)
        with pytest.raises(TypeError):
            coords[0] = 99  # type: ignore[index]

    def test_dict_operations(self, sample_dict: dict[str, int]) -> None:
        """Test basic dict operations with fixture."""
        assert len(sample_dict) == 3
        assert sample_dict["a"] == 1
        assert "b" in sample_dict

    def test_list_operations(self, sample_list: list[int]) -> None:
        """Test basic list operations with fixture."""
        assert len(sample_list) == 5
        assert sum(sample_list) == 15


class TestControlFlow:
    """Test control flow patterns from Chapter 1."""

    def test_list_comprehension(self) -> None:
        """List comprehensions produce correct results."""
        squares = [x**2 for x in range(5)]
        assert squares == [0, 1, 4, 9, 16]

    def test_dict_comprehension(self) -> None:
        """Dict comprehensions produce correct results."""
        squared = {x: x**2 for x in range(4)}
        assert squared == {0: 0, 1: 1, 2: 4, 3: 9}

    def test_filtered_comprehension(self) -> None:
        """Comprehensions with filter conditions."""
        evens = [x for x in range(10) if x % 2 == 0]
        assert evens == [0, 2, 4, 6, 8]


class TestFirstClassFunctions:
    """Test first-class function concepts from Chapter 1."""

    def test_higher_order_function(self) -> None:
        """Functions can be passed as arguments."""

        def apply_twice(func, x: int) -> int:
            return func(func(x))

        result = apply_twice(lambda x: x * 2, 5)
        assert result == 20

    def test_closure(self) -> None:
        """Closures capture enclosing scope variables."""

        def make_adder(n: int):
            def adder(x: int) -> int:
                return x + n

            return adder

        add_five = make_adder(5)
        assert add_five(10) == 15
        assert add_five(0) == 5
