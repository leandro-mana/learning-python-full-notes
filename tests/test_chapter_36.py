"""Tests for Chapter 36: Advanced Testing."""

from unittest.mock import MagicMock, Mock, patch

import pytest


class TestPytestFeatures:
    """Test pytest-specific features."""

    def test_parametrize_squares(self) -> None:
        """parametrize runs a test with multiple inputs."""
        cases = [(1, 1), (2, 4), (3, 9), (4, 16), (0, 0)]
        for value, expected in cases:
            assert value**2 == expected

    def test_fixture_like_setup(self) -> None:
        """Fixtures provide reusable test data."""
        data = {"name": "Alice", "age": 30}
        assert data["name"] == "Alice"
        assert isinstance(data["age"], int)

    def test_tmp_path_usage(self, tmp_path) -> None:
        """tmp_path provides a temporary directory per test."""
        file = tmp_path / "test.txt"
        file.write_text("hello")
        assert file.read_text() == "hello"
        assert file.exists()

    def test_monkeypatch_setattr(self, monkeypatch) -> None:
        """monkeypatch temporarily modifies objects."""

        class Config:
            debug = False

        monkeypatch.setattr(Config, "debug", True)
        assert Config.debug is True

    def test_monkeypatch_env(self, monkeypatch) -> None:
        """monkeypatch can set environment variables."""
        monkeypatch.setenv("TEST_VAR", "hello")
        import os

        assert os.environ["TEST_VAR"] == "hello"

    def test_raises_context(self) -> None:
        """pytest.raises checks for expected exceptions."""
        with pytest.raises(ValueError, match="invalid"):
            raise ValueError("invalid literal")

    def test_approx_for_floats(self) -> None:
        """pytest.approx handles floating point comparison."""
        assert 0.1 + 0.2 == pytest.approx(0.3)
        assert [0.1, 0.2] == pytest.approx([0.1, 0.2])


class TestMocking:
    """Test unittest.mock features."""

    def test_mock_basic(self) -> None:
        """Mock creates callable objects with tracking."""
        m = Mock()
        m(1, 2, key="value")
        m.assert_called_once_with(1, 2, key="value")

    def test_mock_return_value(self) -> None:
        """Mock.return_value controls what mock returns."""
        m = Mock(return_value=42)
        assert m() == 42

    def test_mock_side_effect_exception(self) -> None:
        """side_effect can raise exceptions."""
        m = Mock(side_effect=ValueError("boom"))
        with pytest.raises(ValueError, match="boom"):
            m()

    def test_mock_side_effect_iterable(self) -> None:
        """side_effect can return values from an iterable."""
        m = Mock(side_effect=[1, 2, 3])
        assert m() == 1
        assert m() == 2
        assert m() == 3

    def test_magic_mock_dunder(self) -> None:
        """MagicMock supports dunder methods."""
        m = MagicMock()
        m.__len__.return_value = 5
        assert len(m) == 5

    def test_patch_decorator(self) -> None:
        """patch replaces objects during test."""
        with patch("os.getcwd", return_value="/fake/path"):
            import os

            assert os.getcwd() == "/fake/path"

    def test_mock_call_count(self) -> None:
        """Mock tracks call count."""
        m = Mock()
        m()
        m()
        m()
        assert m.call_count == 3

    def test_mock_spec(self) -> None:
        """spec restricts mock to real object's interface."""
        m = Mock(spec=list)
        m.append(1)  # Valid method
        with pytest.raises(AttributeError):
            m.nonexistent()  # type: ignore[attr-defined]


class TestTestPatterns:
    """Test common testing patterns."""

    def test_arrange_act_assert(self) -> None:
        """AAA pattern structures tests clearly."""
        # Arrange
        items: list[int] = [3, 1, 4, 1, 5]
        # Act
        result = sorted(items)
        # Assert
        assert result == [1, 1, 3, 4, 5]

    def test_test_double_stub(self) -> None:
        """Stubs provide canned responses."""

        class DatabaseStub:
            def query(self, sql: str) -> list[dict]:
                return [{"id": 1, "name": "Alice"}]

        db = DatabaseStub()
        results = db.query("SELECT * FROM users")
        assert len(results) == 1
        assert results[0]["name"] == "Alice"

    def test_test_double_spy(self) -> None:
        """Spies track interactions while delegating."""
        calls: list[str] = []

        class LoggerSpy:
            def log(self, msg: str) -> None:
                calls.append(msg)

        logger = LoggerSpy()
        logger.log("hello")
        logger.log("world")
        assert len(calls) == 2

    def test_builder_pattern_for_test_data(self) -> None:
        """Builder pattern creates complex test objects."""

        class UserBuilder:
            def __init__(self) -> None:
                self._name = "default"
                self._age = 0

            def with_name(self, name: str) -> "UserBuilder":
                self._name = name
                return self

            def with_age(self, age: int) -> "UserBuilder":
                self._age = age
                return self

            def build(self) -> dict:
                return {"name": self._name, "age": self._age}

        user = UserBuilder().with_name("Alice").with_age(30).build()
        assert user == {"name": "Alice", "age": 30}
