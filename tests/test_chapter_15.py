"""Tests for Chapter 15: Design Patterns and Pythonic Code."""

from abc import ABC, abstractmethod
from typing import Protocol


class TestStrategyPattern:
    """Test Strategy pattern implementation."""

    def test_strategy_with_functions(self) -> None:
        """Strategy pattern using first-class functions."""

        def sort_by_name(items: list[dict]) -> list[dict]:
            return sorted(items, key=lambda x: x["name"])

        def sort_by_price(items: list[dict]) -> list[dict]:
            return sorted(items, key=lambda x: x["price"])

        items = [
            {"name": "Banana", "price": 1.50},
            {"name": "Apple", "price": 2.00},
            {"name": "Cherry", "price": 3.00},
        ]

        by_name = sort_by_name(items)
        assert by_name[0]["name"] == "Apple"

        by_price = sort_by_price(items)
        assert by_price[0]["name"] == "Banana"


class TestObserverPattern:
    """Test Observer pattern implementation."""

    def test_observer_notification(self) -> None:
        """Observers are notified of state changes."""
        notifications: list[str] = []

        class EventBus:
            def __init__(self) -> None:
                self._handlers: dict[str, list] = {}

            def subscribe(self, event: str, handler) -> None:
                self._handlers.setdefault(event, []).append(handler)

            def emit(self, event: str, data: str) -> None:
                for handler in self._handlers.get(event, []):
                    handler(data)

        bus = EventBus()
        bus.subscribe("user_created", lambda d: notifications.append(f"email: {d}"))
        bus.subscribe("user_created", lambda d: notifications.append(f"log: {d}"))
        bus.emit("user_created", "Alice")

        assert len(notifications) == 2
        assert "email: Alice" in notifications
        assert "log: Alice" in notifications


class TestFactoryPattern:
    """Test Factory pattern implementation."""

    def test_factory_creates_correct_type(self) -> None:
        """Factory method returns the correct subclass."""

        class Shape(ABC):
            @abstractmethod
            def area(self) -> float: ...

        class Circle(Shape):
            def __init__(self, radius: float) -> None:
                self.radius = radius

            def area(self) -> float:
                return 3.14159 * self.radius**2

        class Square(Shape):
            def __init__(self, side: float) -> None:
                self.side = side

            def area(self) -> float:
                return self.side**2

        registry: dict[str, type] = {"circle": Circle, "square": Square}

        def create_shape(kind: str, **kwargs) -> Shape:
            return registry[kind](**kwargs)

        circle = create_shape("circle", radius=5.0)
        square = create_shape("square", side=4.0)

        assert isinstance(circle, Circle)
        assert isinstance(square, Square)
        assert square.area() == 16.0


class TestProtocolPattern:
    """Test Protocol-based duck typing."""

    def test_protocol_structural_typing(self) -> None:
        """Protocol enables structural typing without inheritance."""

        class Renderable(Protocol):
            def render(self) -> str: ...

        class HtmlWidget:
            def render(self) -> str:
                return "<div>Hello</div>"

        class JsonResponse:
            def render(self) -> str:
                return '{"message": "hello"}'

        def display(item: Renderable) -> str:
            return item.render()

        assert display(HtmlWidget()) == "<div>Hello</div>"
        assert display(JsonResponse()) == '{"message": "hello"}'
