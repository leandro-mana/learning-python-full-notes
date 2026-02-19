"""Tests for Chapter 3: OOP Fundamentals."""

import pytest


class TestClassesAndObjects:
    """Test class creation and basic OOP patterns."""

    def test_class_instantiation(self) -> None:
        """Classes create instances with initialized attributes."""

        class Point:
            def __init__(self, x: float, y: float) -> None:
                self.x = x
                self.y = y

        p = Point(3.0, 4.0)
        assert p.x == 3.0
        assert p.y == 4.0

    def test_dunder_methods(self) -> None:
        """Dunder methods customize object behavior."""

        class Vector:
            def __init__(self, x: float, y: float) -> None:
                self.x = x
                self.y = y

            def __add__(self, other: "Vector") -> "Vector":
                return Vector(self.x + other.x, self.y + other.y)

            def __repr__(self) -> str:
                return f"Vector({self.x}, {self.y})"

        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        v3 = v1 + v2
        assert v3.x == 4
        assert v3.y == 6


class TestInheritance:
    """Test inheritance and method resolution."""

    def test_single_inheritance(self) -> None:
        """Subclasses inherit and can override parent methods."""

        class Animal:
            def speak(self) -> str:
                return "..."

        class Dog(Animal):
            def speak(self) -> str:
                return "Woof!"

        dog = Dog()
        assert dog.speak() == "Woof!"
        assert isinstance(dog, Animal)

    def test_super_calls_parent(self) -> None:
        """super() properly delegates to parent class."""

        class Base:
            def __init__(self, value: int) -> None:
                self.value = value

        class Child(Base):
            def __init__(self, value: int, extra: str) -> None:
                super().__init__(value)
                self.extra = extra

        c = Child(42, "hello")
        assert c.value == 42
        assert c.extra == "hello"


class TestEncapsulation:
    """Test encapsulation and property patterns."""

    def test_property_getter_setter(self) -> None:
        """Properties provide controlled attribute access."""

        class Circle:
            def __init__(self, radius: float) -> None:
                self._radius = radius

            @property
            def radius(self) -> float:
                return self._radius

            @radius.setter
            def radius(self, value: float) -> None:
                if value <= 0:
                    raise ValueError("Radius must be positive")
                self._radius = value

        c = Circle(5.0)
        assert c.radius == 5.0
        c.radius = 10.0
        assert c.radius == 10.0

        with pytest.raises(ValueError):
            c.radius = -1
