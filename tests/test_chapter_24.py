"""Tests for Chapter 24: Metaprogramming."""

import inspect


class TestDynamicAttributes:
    """Test dynamic attribute access."""

    def test_getattr_fallback(self) -> None:
        """__getattr__ is called when normal lookup fails."""

        class DefaultDict:
            def __init__(self, **kwargs: str) -> None:
                self.__dict__.update(kwargs)

            def __getattr__(self, name: str) -> str:
                return f"default_{name}"

        obj = DefaultDict(color="red")
        assert obj.color == "red"
        assert obj.missing == "default_missing"

    def test_setattr_validation(self) -> None:
        """__setattr__ can validate attribute assignments."""

        class Validated:
            def __setattr__(self, name: str, value: object) -> None:
                if name == "age" and isinstance(value, int) and value < 0:
                    raise ValueError("age must be non-negative")
                super().__setattr__(name, value)

        v = Validated()
        v.age = 25
        assert v.age == 25

        try:
            v.age = -1
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_property_dynamic(self) -> None:
        """Properties can be created dynamically."""

        class Circle:
            def __init__(self, radius: float) -> None:
                self._radius = radius

            @property
            def radius(self) -> float:
                return self._radius

            @radius.setter
            def radius(self, value: float) -> None:
                if value < 0:
                    raise ValueError("radius must be non-negative")
                self._radius = value

            @property
            def area(self) -> float:
                return 3.14159 * self._radius**2

        c = Circle(5.0)
        assert c.radius == 5.0
        assert abs(c.area - 78.53975) < 0.001


class TestClassDecorators:
    """Test class decorator patterns."""

    def test_class_decorator_adds_method(self) -> None:
        """Class decorators can add methods to classes."""

        def add_repr(cls):
            def __repr__(self) -> str:
                attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
                return f"{cls.__name__}({attrs})"

            cls.__repr__ = __repr__
            return cls

        @add_repr
        class Point:
            def __init__(self, x: float, y: float) -> None:
                self.x = x
                self.y = y

        p = Point(1.0, 2.0)
        assert "Point(" in repr(p)
        assert "x=1.0" in repr(p)

    def test_init_subclass_registration(self) -> None:
        """__init_subclass__ registers subclasses automatically."""
        registry: list[type] = []

        class Plugin:
            def __init_subclass__(cls, **kwargs: object) -> None:
                super().__init_subclass__(**kwargs)
                registry.append(cls)

        class AuthPlugin(Plugin):
            pass

        class CachePlugin(Plugin):
            pass

        assert len(registry) == 2
        assert AuthPlugin in registry
        assert CachePlugin in registry


class TestIntrospection:
    """Test inspect module capabilities."""

    def test_inspect_signature(self) -> None:
        """inspect.signature reveals function parameters."""

        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        sig = inspect.signature(greet)
        params = list(sig.parameters.keys())
        assert params == ["name", "greeting"]
        assert sig.parameters["greeting"].default == "Hello"

    def test_inspect_members(self) -> None:
        """inspect.getmembers lists object attributes."""

        class MyClass:
            x: int = 10

            def method(self) -> None:
                pass

        methods = [name for name, _ in inspect.getmembers(MyClass, predicate=inspect.isfunction)]
        assert "method" in methods

    def test_inspect_source(self) -> None:
        """inspect.getsource retrieves source code."""

        def add(a: int, b: int) -> int:
            return a + b

        source = inspect.getsource(add)
        assert "def add" in source
        assert "return a + b" in source

    def test_inspect_isclass_isfunction(self) -> None:
        """inspect provides type-checking predicates."""

        class Foo:
            pass

        def bar() -> None:
            pass

        assert inspect.isclass(Foo)
        assert inspect.isfunction(bar)
        assert not inspect.isclass(bar)
        assert not inspect.isfunction(Foo)
