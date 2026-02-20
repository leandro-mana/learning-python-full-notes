"""Tests for Chapter 16: Type Hints and Static Analysis."""

from typing import (
    Generic,
    Literal,
    Protocol,
    TypeVar,
    get_type_hints,
    overload,
    runtime_checkable,
)


class TestAnnotationFundamentals:
    """Test basic type annotation patterns."""

    def test_function_annotations(self) -> None:
        """Functions store type hints in __annotations__."""

        def greet(name: str, times: int = 1) -> str:
            return (name + "! ") * times

        hints = get_type_hints(greet)
        assert hints["name"] is str
        assert hints["times"] is int
        assert hints["return"] is str
        assert greet("Hello", 2) == "Hello! Hello! "

    def test_variable_annotations(self) -> None:
        """Variable annotations are stored in the class/module."""
        x: int = 42
        y: str = "hello"
        assert isinstance(x, int)
        assert isinstance(y, str)

    def test_generic_types(self) -> None:
        """Built-in generics allow parameterized types."""
        numbers: list[int] = [1, 2, 3]
        mapping: dict[str, int] = {"a": 1, "b": 2}
        pair: tuple[str, int] = ("hello", 42)

        assert numbers == [1, 2, 3]
        assert mapping["a"] == 1
        assert pair == ("hello", 42)


class TestAdvancedTyping:
    """Test advanced typing features."""

    def test_typevar_generic_function(self) -> None:
        """TypeVar enables generic functions."""
        T = TypeVar("T")

        def first(items: list[T]) -> T:
            return items[0]

        assert first([1, 2, 3]) == 1
        assert first(["a", "b"]) == "a"

    def test_generic_class(self) -> None:
        """Generic classes are parameterized with TypeVar."""
        T = TypeVar("T")

        class Stack(Generic[T]):
            def __init__(self) -> None:
                self._items: list[T] = []

            def push(self, item: T) -> None:
                self._items.append(item)

            def pop(self) -> T:
                return self._items.pop()

            def is_empty(self) -> bool:
                return len(self._items) == 0

        stack: Stack[int] = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2
        assert stack.pop() == 1
        assert stack.is_empty()

    def test_protocol_structural_typing(self) -> None:
        """Protocol enables structural subtyping."""

        @runtime_checkable
        class Drawable(Protocol):
            def draw(self) -> str: ...

        class Circle:
            def draw(self) -> str:
                return "Drawing circle"

        class Square:
            def draw(self) -> str:
                return "Drawing square"

        def render(shape: Drawable) -> str:
            return shape.draw()

        assert render(Circle()) == "Drawing circle"
        assert render(Square()) == "Drawing square"
        assert isinstance(Circle(), Drawable)

    def test_overload_signatures(self) -> None:
        """@overload documents multiple call signatures."""

        @overload
        def process(data: str) -> list[str]: ...
        @overload
        def process(data: list[str]) -> str: ...

        def process(data: str | list[str]) -> list[str] | str:
            if isinstance(data, str):
                return data.split()
            return " ".join(data)

        assert process("hello world") == ["hello", "world"]
        assert process(["hello", "world"]) == "hello world"

    def test_literal_type(self) -> None:
        """Literal restricts values to specific constants."""

        def set_color(color: Literal["red", "green", "blue"]) -> str:
            return f"Color set to {color}"

        assert set_color("red") == "Color set to red"
        assert set_color("blue") == "Color set to blue"
