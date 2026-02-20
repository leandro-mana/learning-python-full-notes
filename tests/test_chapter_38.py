"""Tests for Chapter 38: Memory Management."""

import gc
import sys
import tracemalloc
import weakref


class TestReferenceCounting:
    """Test reference counting mechanics."""

    def test_getrefcount(self) -> None:
        """sys.getrefcount returns the reference count (includes the call itself)."""
        a: list[int] = []
        count = sys.getrefcount(a)
        assert count >= 2  # a + getrefcount arg

    def test_multiple_references(self) -> None:
        """Multiple names increase reference count."""
        a: list[int] = []
        base = sys.getrefcount(a)
        b = a  # noqa: F841
        assert sys.getrefcount(a) == base + 1

    def test_del_decreases_refcount(self) -> None:
        """del removes a reference."""
        a: list[int] = []
        b = a
        base = sys.getrefcount(a)
        del b
        assert sys.getrefcount(a) == base - 1

    def test_container_references(self) -> None:
        """Containers hold references to their items."""
        obj: list[int] = []
        base = sys.getrefcount(obj)
        container = [obj]  # noqa: F841
        assert sys.getrefcount(obj) == base + 1


class TestGarbageCollection:
    """Test gc module for cycle detection."""

    def test_gc_is_enabled(self) -> None:
        """gc is enabled by default."""
        assert gc.isenabled()

    def test_gc_collect(self) -> None:
        """gc.collect runs garbage collection."""
        collected = gc.collect()
        assert isinstance(collected, int)

    def test_circular_reference_cleanup(self) -> None:
        """gc handles circular references."""

        class Node:
            def __init__(self) -> None:
                self.ref: "Node | None" = None

        a = Node()
        b = Node()
        a.ref = b
        b.ref = a
        weak_a = weakref.ref(a)
        del a, b
        gc.collect()
        assert weak_a() is None

    def test_gc_get_stats(self) -> None:
        """gc.get_stats returns collection statistics."""
        stats = gc.get_stats()
        assert len(stats) == 3  # 3 generations
        assert "collections" in stats[0]
        assert "collected" in stats[0]

    def test_gc_freeze(self) -> None:
        """gc.freeze moves objects to permanent generation."""
        gc.freeze()
        frozen_count = gc.get_freeze_count()
        assert frozen_count >= 0
        gc.unfreeze()

    def test_weakref_finalize(self) -> None:
        """weakref.finalize runs a callback when object is collected."""
        cleaned_up = []

        class Resource:
            pass

        obj = Resource()
        weakref.finalize(obj, lambda: cleaned_up.append(True))
        del obj
        gc.collect()
        assert len(cleaned_up) == 1


class TestMemoryProfiling:
    """Test memory inspection tools."""

    def test_getsizeof(self) -> None:
        """sys.getsizeof returns memory size in bytes."""
        assert sys.getsizeof(0) > 0
        assert sys.getsizeof([]) < sys.getsizeof([1, 2, 3, 4, 5])

    def test_getsizeof_types(self) -> None:
        """Different types have different base sizes."""
        assert sys.getsizeof("") < sys.getsizeof("hello world")
        assert sys.getsizeof(()) < sys.getsizeof((1, 2, 3))

    def test_tracemalloc_snapshot(self) -> None:
        """tracemalloc tracks memory allocations."""
        tracemalloc.start()
        try:
            _data = [i for i in range(1000)]  # noqa: C416
            snapshot = tracemalloc.take_snapshot()
            stats = snapshot.statistics("lineno")
            assert len(stats) > 0
        finally:
            tracemalloc.stop()

    def test_tracemalloc_get_traced_memory(self) -> None:
        """tracemalloc reports current and peak memory."""
        tracemalloc.start()
        try:
            current, peak = tracemalloc.get_traced_memory()
            assert current >= 0
            assert peak >= 0
            assert peak >= current
        finally:
            tracemalloc.stop()

    def test_slots_memory_savings(self) -> None:
        """__slots__ reduces per-instance memory."""

        class Regular:
            def __init__(self, x: int) -> None:
                self.x = x

        class Slotted:
            __slots__ = ("x",)

            def __init__(self, x: int) -> None:
                self.x = x

        regular = Regular(1)
        slotted = Slotted(1)
        assert sys.getsizeof(slotted) < sys.getsizeof(regular)
