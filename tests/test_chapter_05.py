"""Tests for Chapter 5: Decorators, Generators, and Context Managers."""

from functools import wraps
from typing import Any, Callable, Generator


class TestDecorators:
    """Test decorator patterns."""

    def test_basic_decorator(self) -> None:
        """Basic decorator wraps function behavior."""
        call_log: list[str] = []

        def log_calls(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                call_log.append(func.__name__)
                return func(*args, **kwargs)

            return wrapper

        @log_calls
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        result = greet("Alice")
        assert result == "Hello, Alice!"
        assert call_log == ["greet"]

    def test_wraps_preserves_metadata(self) -> None:
        """@wraps preserves original function metadata."""

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)

            return wrapper

        @decorator
        def my_func():
            """My docstring."""
            pass

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "My docstring."

    def test_parameterized_decorator(self) -> None:
        """Decorator factories accept arguments."""

        def repeat(times: int) -> Callable:
            def decorator(func: Callable) -> Callable:
                @wraps(func)
                def wrapper(*args: Any, **kwargs: Any) -> list[Any]:
                    return [func(*args, **kwargs) for _ in range(times)]

                return wrapper

            return decorator

        @repeat(times=3)
        def echo(msg: str) -> str:
            return msg

        assert echo("hi") == ["hi", "hi", "hi"]


class TestGenerators:
    """Test generator patterns."""

    def test_basic_generator(self) -> None:
        """Generator functions yield values lazily."""

        def countdown(n: int) -> Generator[int, None, None]:
            while n > 0:
                yield n
                n -= 1

        result = list(countdown(3))
        assert result == [3, 2, 1]

    def test_generator_expression(self) -> None:
        """Generator expressions are memory-efficient."""
        gen = (x**2 for x in range(5))
        assert list(gen) == [0, 1, 4, 9, 16]

    def test_generator_is_lazy(self) -> None:
        """Generators compute values on demand."""
        side_effects: list[int] = []

        def tracked_range(n: int) -> Generator[int, None, None]:
            for i in range(n):
                side_effects.append(i)
                yield i

        gen = tracked_range(5)
        assert side_effects == []  # nothing computed yet
        next(gen)
        assert side_effects == [0]  # only first value computed


class TestContextManagers:
    """Test context manager patterns."""

    def test_basic_context_manager(self) -> None:
        """Context managers run enter/exit around with block."""
        events: list[str] = []

        class Tracker:
            def __enter__(self):
                events.append("enter")
                return self

            def __exit__(self, *args):
                events.append("exit")

        with Tracker():
            events.append("body")

        assert events == ["enter", "body", "exit"]

    def test_contextmanager_decorator(self) -> None:
        """@contextmanager simplifies context manager creation."""
        from contextlib import contextmanager

        events: list[str] = []

        @contextmanager
        def tracked():
            events.append("setup")
            yield "resource"
            events.append("teardown")

        with tracked() as value:
            events.append(f"using {value}")

        assert events == ["setup", "using resource", "teardown"]
