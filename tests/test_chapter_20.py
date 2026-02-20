"""Tests for Chapter 20: Python Internals and Performance."""

import dis
import gc
import sys
import weakref
from io import StringIO


class TestMemoryModel:
    """Test Python memory model concepts."""

    def test_id_and_identity(self) -> None:
        """id() returns unique identity; 'is' checks identity."""
        a = [1, 2, 3]
        b = a
        c = [1, 2, 3]

        assert a is b  # Same object
        assert a is not c  # Different objects
        assert a == c  # Equal values
        assert id(a) == id(b)
        assert id(a) != id(c)

    def test_small_integer_interning(self) -> None:
        """CPython interns small integers (-5 to 256)."""
        a = 256
        b = 256
        assert a is b  # Interned

    def test_sys_getsizeof(self) -> None:
        """sys.getsizeof returns object memory in bytes."""
        empty_list = []
        small_list = [1, 2, 3]
        assert sys.getsizeof(empty_list) < sys.getsizeof(small_list)

        empty_dict: dict = {}
        assert sys.getsizeof(empty_dict) > 0

    def test_sys_getrefcount(self) -> None:
        """sys.getrefcount shows reference count (includes the call arg)."""
        a = [1, 2, 3]
        count = sys.getrefcount(a)
        assert count >= 2  # 'a' + argument to getrefcount


class TestGarbageCollection:
    """Test garbage collection behavior."""

    def test_reference_counting(self) -> None:
        """Objects are freed when reference count reaches zero."""
        deleted: list[bool] = []

        class Tracked:
            def __del__(self) -> None:
                deleted.append(True)

        obj = Tracked()
        assert len(deleted) == 0
        del obj
        # After del, __del__ should have been called
        assert len(deleted) == 1

    def test_weakref_doesnt_prevent_gc(self) -> None:
        """Weak references don't prevent garbage collection."""

        class MyObj:
            pass

        obj = MyObj()
        ref = weakref.ref(obj)
        assert ref() is obj

        del obj
        gc.collect()
        assert ref() is None  # Object was collected

    def test_gc_cycle_detection(self) -> None:
        """gc module detects and collects reference cycles."""

        class Node:
            def __init__(self) -> None:
                self.ref: "Node | None" = None

        a = Node()
        b = Node()
        a.ref = b
        b.ref = a  # Circular reference

        del a, b
        collected = gc.collect()
        assert collected >= 0  # gc handled the cycle


class TestSlotsOptimization:
    """Test __slots__ for memory efficiency."""

    def test_slots_restricts_attributes(self) -> None:
        """__slots__ restricts which attributes can be set."""

        class Point:
            __slots__ = ("x", "y")

            def __init__(self, x: float, y: float) -> None:
                self.x = x
                self.y = y

        p = Point(1.0, 2.0)
        assert p.x == 1.0
        assert not hasattr(p, "__dict__")

    def test_slots_saves_memory(self) -> None:
        """Slotted classes use less memory than regular classes."""

        class Regular:
            def __init__(self, x: float, y: float) -> None:
                self.x = x
                self.y = y

        class Slotted:
            __slots__ = ("x", "y")

            def __init__(self, x: float, y: float) -> None:
                self.x = x
                self.y = y

        regular = Regular(1.0, 2.0)
        slotted = Slotted(1.0, 2.0)
        assert sys.getsizeof(slotted) <= sys.getsizeof(regular)


class TestBytecodeInspection:
    """Test dis module for bytecode inspection."""

    def test_dis_produces_output(self) -> None:
        """dis.dis disassembles functions to bytecode."""

        def add(a: int, b: int) -> int:
            return a + b

        output = StringIO()
        dis.dis(add, file=output)
        bytecode = output.getvalue()
        assert "RETURN_VALUE" in bytecode

    def test_code_object_attributes(self) -> None:
        """Function code objects expose bytecode metadata."""

        def example(x: int, y: int) -> int:
            z = x + y
            return z * 2

        code = example.__code__
        assert code.co_argcount == 2
        assert "x" in code.co_varnames
        assert "y" in code.co_varnames
        assert "z" in code.co_varnames
