"""Tests for Chapter 39: C Interoperability."""

import array
import ctypes
import struct


class TestCtypesBasics:
    """Test ctypes fundamental types and operations."""

    def test_ctypes_int(self) -> None:
        """ctypes provides C-compatible integer types."""
        i = ctypes.c_int(42)
        assert i.value == 42

    def test_ctypes_float(self) -> None:
        """ctypes provides C-compatible float types."""
        f = ctypes.c_float(3.14)
        assert abs(f.value - 3.14) < 0.01

    def test_ctypes_char_array(self) -> None:
        """ctypes can create fixed-size char arrays."""
        buf = ctypes.create_string_buffer(10)
        assert len(buf) == 10
        buf.value = b"hello"
        assert buf.value == b"hello"

    def test_ctypes_pointer(self) -> None:
        """ctypes supports pointer operations."""
        i = ctypes.c_int(42)
        p = ctypes.pointer(i)
        assert p.contents.value == 42
        p.contents.value = 100
        assert i.value == 100

    def test_ctypes_sizeof(self) -> None:
        """ctypes.sizeof returns type sizes."""
        assert ctypes.sizeof(ctypes.c_int) == 4
        assert ctypes.sizeof(ctypes.c_double) == 8
        assert ctypes.sizeof(ctypes.c_char) == 1


class TestCtypesAdvanced:
    """Test ctypes structures and arrays."""

    def test_ctypes_structure(self) -> None:
        """ctypes.Structure defines C-compatible structs."""

        class Point(ctypes.Structure):
            _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]

        p = Point(10, 20)
        assert p.x == 10
        assert p.y == 20

    def test_ctypes_structure_sizeof(self) -> None:
        """Structure size matches C layout."""

        class Pair(ctypes.Structure):
            _fields_ = [("a", ctypes.c_int), ("b", ctypes.c_int)]

        assert ctypes.sizeof(Pair) == 8  # Two 4-byte ints

    def test_ctypes_array(self) -> None:
        """ctypes arrays hold fixed-count elements."""
        IntArray5 = ctypes.c_int * 5
        arr = IntArray5(1, 2, 3, 4, 5)
        assert arr[0] == 1
        assert arr[4] == 5
        assert len(arr) == 5

    def test_ctypes_union(self) -> None:
        """ctypes.Union overlaps fields in memory."""

        class IntOrFloat(ctypes.Union):
            _fields_ = [("i", ctypes.c_int), ("f", ctypes.c_float)]

        u = IntOrFloat()
        u.i = 0
        assert u.f == 0.0  # Same memory

    def test_ctypes_callback(self) -> None:
        """CFUNCTYPE creates C-callable function pointers."""
        CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)

        def py_add(a: int, b: int) -> int:
            return a + b

        cb = CALLBACK(py_add)
        assert cb(3, 4) == 7


class TestArrayAndMemoryview:
    """Test array module and memoryview."""

    def test_array_creation(self) -> None:
        """array.array creates typed numeric arrays."""
        a = array.array("i", [1, 2, 3, 4, 5])
        assert len(a) == 5
        assert a[0] == 1
        assert a.typecode == "i"

    def test_array_itemsize(self) -> None:
        """array.itemsize shows bytes per element."""
        a = array.array("i")  # signed int
        assert a.itemsize == struct.calcsize("i")

    def test_array_buffer_info(self) -> None:
        """buffer_info returns address and length."""
        a = array.array("d", [1.0, 2.0, 3.0])
        address, length = a.buffer_info()
        assert length == 3
        assert address > 0

    def test_array_bytes_conversion(self) -> None:
        """Arrays convert to/from bytes."""
        a = array.array("i", [1, 2, 3])
        b = a.tobytes()
        a2 = array.array("i")
        a2.frombytes(b)
        assert list(a) == list(a2)

    def test_memoryview_basic(self) -> None:
        """memoryview provides zero-copy access to buffer data."""
        data = bytearray(b"Hello, World!")
        mv = memoryview(data)
        assert bytes(mv[0:5]) == b"Hello"

    def test_memoryview_modify(self) -> None:
        """memoryview can modify the underlying buffer."""
        data = bytearray(b"Hello")
        mv = memoryview(data)
        mv[0] = ord("J")
        assert data == bytearray(b"Jello")

    def test_memoryview_format(self) -> None:
        """memoryview exposes format and shape info."""
        a = array.array("i", [1, 2, 3])
        mv = memoryview(a)
        assert mv.format == "i"
        assert mv.itemsize == struct.calcsize("i")
        assert len(mv) == 3

    def test_struct_pack_unpack(self) -> None:
        """struct packs/unpacks binary data."""
        packed = struct.pack("!2I", 1, 2)  # network byte order, 2 unsigned ints
        a, b = struct.unpack("!2I", packed)
        assert a == 1
        assert b == 2
