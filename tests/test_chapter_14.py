"""Tests for Chapter 14: Data Structures and Collections."""

from collections import ChainMap, Counter, defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, auto


class TestCollections:
    """Test collections module types."""

    def test_counter_counts(self) -> None:
        """Counter counts hashable elements."""
        counter = Counter("abracadabra")
        assert counter["a"] == 5
        assert counter["b"] == 2
        assert counter.most_common(2) == [("a", 5), ("b", 2)]

    def test_defaultdict_provides_defaults(self) -> None:
        """defaultdict provides default values for missing keys."""
        dd: defaultdict[str, list[int]] = defaultdict(list)
        dd["a"].append(1)
        dd["a"].append(2)
        dd["b"].append(3)
        assert dd["a"] == [1, 2]
        assert dd["c"] == []  # Auto-created with default

    def test_deque_operations(self) -> None:
        """deque supports efficient append/pop from both ends."""
        d: deque[int] = deque([1, 2, 3])
        d.appendleft(0)
        d.append(4)
        assert list(d) == [0, 1, 2, 3, 4]

        d.popleft()
        d.pop()
        assert list(d) == [1, 2, 3]

    def test_deque_maxlen(self) -> None:
        """deque with maxlen keeps only the most recent items."""
        d: deque[int] = deque(maxlen=3)
        for i in range(5):
            d.append(i)
        assert list(d) == [2, 3, 4]

    def test_chainmap_layered_lookup(self) -> None:
        """ChainMap searches multiple dicts in order."""
        defaults = {"color": "blue", "size": "medium"}
        overrides = {"color": "red"}
        config = ChainMap(overrides, defaults)

        assert config["color"] == "red"  # From overrides
        assert config["size"] == "medium"  # From defaults


class TestDataclasses:
    """Test dataclass patterns."""

    def test_basic_dataclass(self) -> None:
        """Dataclasses auto-generate __init__, __repr__, __eq__."""

        @dataclass
        class Point:
            x: float
            y: float

        p1 = Point(1.0, 2.0)
        p2 = Point(1.0, 2.0)
        assert p1 == p2
        assert "Point(x=1.0, y=2.0)" in repr(p1)

    def test_frozen_dataclass(self) -> None:
        """Frozen dataclasses are immutable."""

        @dataclass(frozen=True)
        class Color:
            r: int
            g: int
            b: int

        red = Color(255, 0, 0)
        assert red.r == 255
        # frozen=True makes instances hashable
        assert hash(red) is not None

    def test_dataclass_field_defaults(self) -> None:
        """field() provides default factories for mutable defaults."""

        @dataclass
        class Config:
            name: str
            tags: list[str] = field(default_factory=list)

        c1 = Config("app1")
        c2 = Config("app2")
        c1.tags.append("web")
        assert c1.tags == ["web"]
        assert c2.tags == []  # Independent lists


class TestEnums:
    """Test enum patterns."""

    def test_basic_enum(self) -> None:
        """Enums provide named constants."""

        class Color(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        assert Color.RED.value == 1
        assert Color.RED.name == "RED"
        assert Color(2) is Color.GREEN

    def test_auto_values(self) -> None:
        """auto() generates values automatically."""

        class Direction(Enum):
            NORTH = auto()
            SOUTH = auto()
            EAST = auto()
            WEST = auto()

        assert len(Direction) == 4
        assert Direction.NORTH.value == 1

    def test_enum_iteration(self) -> None:
        """Enums are iterable."""

        class Status(Enum):
            PENDING = "pending"
            ACTIVE = "active"
            CLOSED = "closed"

        names = [s.name for s in Status]
        assert names == ["PENDING", "ACTIVE", "CLOSED"]
