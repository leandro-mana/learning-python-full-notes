"""Tests for Chapter 4: Advanced OOP - Classes and Inheritance."""

from abc import ABC, abstractmethod

import pytest


class TestMultipleInheritanceAndMRO:
    """Test multiple inheritance and Method Resolution Order."""

    def test_mro_diamond(self) -> None:
        """MRO resolves diamond inheritance correctly."""

        class A:
            def method(self) -> str:
                return "A"

        class B(A):
            def method(self) -> str:
                return "B"

        class C(A):
            def method(self) -> str:
                return "C"

        class D(B, C):
            pass

        d = D()
        assert d.method() == "B"
        assert D.__mro__ == (D, B, C, A, object)

    def test_super_chain(self) -> None:
        """super() follows MRO for cooperative multiple inheritance."""

        class Base:
            def __init__(self) -> None:
                self.calls: list[str] = []

        class A(Base):
            def __init__(self) -> None:
                super().__init__()
                self.calls.append("A")

        class B(Base):
            def __init__(self) -> None:
                super().__init__()
                self.calls.append("B")

        class C(A, B):
            def __init__(self) -> None:
                super().__init__()
                self.calls.append("C")

        c = C()
        assert "A" in c.calls
        assert "B" in c.calls
        assert "C" in c.calls


class TestMetaclasses:
    """Test metaclass patterns."""

    def test_singleton_metaclass(self) -> None:
        """Singleton metaclass ensures only one instance."""

        class SingletonMeta(type):
            _instances: dict[type, object] = {}

            def __call__(cls, *args, **kwargs):
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
                return cls._instances[cls]

        class Singleton(metaclass=SingletonMeta):
            pass

        a = Singleton()
        b = Singleton()
        assert a is b


class TestDescriptors:
    """Test descriptor protocol."""

    def test_data_descriptor(self) -> None:
        """Data descriptors intercept attribute access."""

        class Positive:
            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                return obj.__dict__.get(self.name, 0)

            def __set__(self, obj, value):
                if value < 0:
                    raise ValueError(f"{self.name} must be positive")
                obj.__dict__[self.name] = value

        class Account:
            balance = Positive()

            def __init__(self, balance: float) -> None:
                self.balance = balance

        acc = Account(100)
        assert acc.balance == 100

        with pytest.raises(ValueError):
            acc.balance = -50


class TestAbstractBaseClasses:
    """Test ABC patterns."""

    def test_cannot_instantiate_abc(self) -> None:
        """Abstract classes cannot be instantiated directly."""

        class Shape(ABC):
            @abstractmethod
            def area(self) -> float:
                pass

        with pytest.raises(TypeError):
            Shape()  # type: ignore[abstract]

    def test_concrete_implementation(self) -> None:
        """Concrete subclasses must implement all abstract methods."""

        class Shape(ABC):
            @abstractmethod
            def area(self) -> float:
                pass

        class Square(Shape):
            def __init__(self, side: float) -> None:
                self.side = side

            def area(self) -> float:
                return self.side**2

        s = Square(5)
        assert s.area() == 25
        assert isinstance(s, Shape)
