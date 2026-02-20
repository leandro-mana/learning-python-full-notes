"""Tests for Chapter 35: Advanced Python Patterns."""

import copy
import weakref
from abc import ABC, abstractmethod


class TestDescriptorsDeepDive:
    """Test descriptor protocol patterns."""

    def test_data_descriptor(self) -> None:
        """Data descriptors have __set__ and control attribute access."""

        class Validated:
            def __set_name__(self, owner: type, name: str) -> None:
                self.name = name

            def __get__(self, obj: object, objtype: type | None = None) -> object:
                if obj is None:
                    return self
                return obj.__dict__.get(self.name)

            def __set__(self, obj: object, value: object) -> None:
                if not isinstance(value, int) or value < 0:
                    raise ValueError(f"{self.name} must be a non-negative int")
                obj.__dict__[self.name] = value

        class Order:
            quantity = Validated()

        order = Order()
        order.quantity = 10
        assert order.quantity == 10

        try:
            order.quantity = -1
            assert False, "Should have raised"
        except ValueError:
            pass

    def test_non_data_descriptor(self) -> None:
        """Non-data descriptors only have __get__."""

        class CachedProperty:
            def __init__(self, func):
                self.func = func
                self.name = func.__name__

            def __get__(self, obj: object, objtype: type | None = None):
                if obj is None:
                    return self
                value = self.func(obj)
                obj.__dict__[self.name] = value  # Cache in instance
                return value

        class Circle:
            def __init__(self, radius: float) -> None:
                self.radius = radius

            @CachedProperty
            def area(self) -> float:
                return 3.14159 * self.radius**2

        c = Circle(5.0)
        assert abs(c.area - 78.53975) < 0.001
        assert "area" in c.__dict__  # Cached in instance

    def test_descriptor_set_name(self) -> None:
        """__set_name__ is called when descriptor is assigned to class."""
        names: list[str] = []

        class Tracker:
            def __set_name__(self, owner: type, name: str) -> None:
                names.append(name)

            def __get__(self, obj: object, objtype: type | None = None) -> object:
                return None

        class MyClass:
            x = Tracker()
            y = Tracker()

        assert names == ["x", "y"]


class TestSlotsAndWeakrefs:
    """Test __slots__ and weakref patterns."""

    def test_slots_restricts_attributes(self) -> None:
        """__slots__ restricts which attributes can be set."""

        class Point:
            __slots__ = ("x", "y")

        p = Point()
        p.x = 1
        p.y = 2
        assert p.x == 1

        try:
            p.z = 3  # type: ignore[attr-defined]
            assert False, "Should have raised"
        except AttributeError:
            pass

    def test_slots_no_dict(self) -> None:
        """Slotted classes have no __dict__ by default."""

        class Slotted:
            __slots__ = ("value",)

        obj = Slotted()
        assert not hasattr(obj, "__dict__")

    def test_weakref_basic(self) -> None:
        """weakref.ref creates a weak reference."""

        class MyObj:
            pass

        obj = MyObj()
        ref = weakref.ref(obj)
        assert ref() is obj
        del obj
        assert ref() is None

    def test_weak_value_dictionary(self) -> None:
        """WeakValueDictionary auto-removes garbage-collected values."""

        class Item:
            def __init__(self, name: str) -> None:
                self.name = name

        cache: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        item = Item("test")
        cache["key"] = item
        assert cache["key"].name == "test"
        del item
        assert "key" not in cache


class TestABCAndCopyProtocol:
    """Test ABCs, virtual subclasses, and copy protocol."""

    def test_abc_cannot_instantiate(self) -> None:
        """ABCs with abstract methods can't be instantiated."""

        class Shape(ABC):
            @abstractmethod
            def area(self) -> float: ...

        try:
            Shape()  # type: ignore[abstract]
            assert False, "Should have raised"
        except TypeError:
            pass

    def test_abc_concrete_subclass(self) -> None:
        """Concrete subclasses implement all abstract methods."""

        class Shape(ABC):
            @abstractmethod
            def area(self) -> float: ...

        class Square(Shape):
            def __init__(self, side: float) -> None:
                self.side = side

            def area(self) -> float:
                return self.side**2

        s = Square(4.0)
        assert s.area() == 16.0
        assert isinstance(s, Shape)

    def test_abc_register_virtual(self) -> None:
        """register creates virtual subclasses without inheritance."""

        class Drawable(ABC):
            @abstractmethod
            def draw(self) -> str: ...

        class Circle:
            def draw(self) -> str:
                return "O"

        Drawable.register(Circle)
        assert isinstance(Circle(), Drawable)
        assert issubclass(Circle, Drawable)
        assert Circle.__mro__ == (Circle, object)  # No Drawable in MRO

    def test_copy_shallow(self) -> None:
        """copy.copy creates a shallow copy."""
        original = [[1, 2], [3, 4]]
        shallow = copy.copy(original)
        assert shallow == original
        assert shallow is not original
        assert shallow[0] is original[0]  # Same inner list

    def test_copy_deep(self) -> None:
        """copy.deepcopy creates a fully independent copy."""
        original = [[1, 2], [3, 4]]
        deep = copy.deepcopy(original)
        assert deep == original
        assert deep is not original
        assert deep[0] is not original[0]  # Different inner list

    def test_custom_copy(self) -> None:
        """__copy__ customizes shallow copy behavior."""

        class Config:
            def __init__(self, settings: dict) -> None:
                self.settings = settings
                self.copy_count = 0

            def __copy__(self):
                new = Config(self.settings.copy())
                new.copy_count = self.copy_count + 1
                return new

        c1 = Config({"debug": True})
        c2 = copy.copy(c1)
        assert c2.settings == {"debug": True}
        assert c2.copy_count == 1
        assert c2.settings is not c1.settings
