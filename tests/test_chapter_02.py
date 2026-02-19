"""Tests for Chapter 2: Type System and Variables."""


class TestVariablesAndBinding:
    """Test variable binding and reference concepts."""

    def test_aliasing(self) -> None:
        """Assignment creates references, not copies."""
        a: list[int] = [1, 2, 3]
        b = a  # b is an alias for the same object
        b.append(4)
        assert a == [1, 2, 3, 4]  # a is affected

    def test_shallow_copy(self) -> None:
        """Shallow copy creates independent top-level container."""
        original: list[int] = [1, 2, 3]
        copied = original.copy()
        copied.append(4)
        assert original == [1, 2, 3]  # original unchanged

    def test_immutable_rebinding(self) -> None:
        """Rebinding immutable types creates new objects."""
        x: int = 10
        original_id = id(x)
        x = x + 1
        assert x == 11
        assert id(x) != original_id


class TestScopeAndNamespaces:
    """Test LEGB rule and scoping."""

    def test_legb_rule(self) -> None:
        """Local scope takes precedence over enclosing/global."""

        def outer():
            def inner():
                local_var = "local"
                return local_var

            return inner()

        assert outer() == "local"

    def test_nonlocal_keyword(self) -> None:
        """nonlocal allows modifying enclosing scope variable."""

        def counter():
            count = 0

            def increment():
                nonlocal count
                count += 1
                return count

            return increment

        inc = counter()
        assert inc() == 1
        assert inc() == 2
        assert inc() == 3


class TestTypeAnnotations:
    """Test type annotation patterns."""

    def test_optional_type(self) -> None:
        """Optional types can be None."""
        value: str | None = None
        assert value is None
        value = "hello"
        assert value == "hello"

    def test_generic_container(self) -> None:
        """Generic type annotations describe container contents."""
        items: list[int] = [1, 2, 3]
        assert all(isinstance(x, int) for x in items)
