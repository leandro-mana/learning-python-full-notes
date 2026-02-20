"""Tests for Chapter 25: Python Ecosystem and Best Practices."""

import ast
import textwrap
from typing import Protocol


class TestCodeStyle:
    """Test code style concepts."""

    def test_pep8_naming_conventions(self) -> None:
        """PEP 8 naming conventions are standard Python style."""
        # snake_case for functions and variables
        my_variable = 42
        assert my_variable == 42

        # PascalCase for classes
        class MyClass:
            pass

        assert MyClass.__name__ == "MyClass"

        # UPPER_SNAKE_CASE for constants
        MAX_RETRIES = 3
        assert MAX_RETRIES == 3

    def test_docstring_access(self) -> None:
        """Docstrings are accessible via __doc__."""

        def my_function() -> str:
            """This function returns a greeting."""
            return "hello"

        assert my_function.__doc__ is not None
        assert "greeting" in my_function.__doc__

    def test_textwrap_dedent(self) -> None:
        """textwrap.dedent cleans up indented strings."""
        indented = """\
            Line 1
            Line 2
            Line 3"""
        cleaned = textwrap.dedent(indented)
        assert cleaned == "Line 1\nLine 2\nLine 3"


class TestTestingPatterns:
    """Test pytest patterns and best practices."""

    def test_parametrize_concept(self) -> None:
        """Parameterized tests cover multiple cases."""
        cases = [
            (2, 3, 5),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300),
        ]
        for a, b, expected in cases:
            assert a + b == expected

    def test_fixture_concept(self) -> None:
        """Fixtures provide reusable test setup."""

        def create_user(name: str = "Alice", age: int = 30) -> dict:
            return {"name": name, "age": age, "active": True}

        user = create_user()
        assert user["name"] == "Alice"
        assert user["active"] is True

        custom_user = create_user("Bob", 25)
        assert custom_user["name"] == "Bob"

    def test_protocol_for_testability(self) -> None:
        """Protocols enable easy mocking and testing."""

        class DataStore(Protocol):
            def get(self, key: str) -> str | None: ...
            def put(self, key: str, value: str) -> None: ...

        class InMemoryStore:
            def __init__(self) -> None:
                self._data: dict[str, str] = {}

            def get(self, key: str) -> str | None:
                return self._data.get(key)

            def put(self, key: str, value: str) -> None:
                self._data[key] = value

        store: DataStore = InMemoryStore()
        store.put("key1", "value1")
        assert store.get("key1") == "value1"
        assert store.get("missing") is None


class TestASTAndCodeAnalysis:
    """Test AST-based code analysis."""

    def test_ast_parse(self) -> None:
        """ast.parse creates an AST from source code."""
        source = "x = 1 + 2"
        tree = ast.parse(source)
        assert isinstance(tree, ast.Module)
        assert len(tree.body) == 1
        assert isinstance(tree.body[0], ast.Assign)

    def test_ast_walk_finds_functions(self) -> None:
        """ast.walk traverses all nodes in the AST."""
        source = textwrap.dedent("""\
            def foo():
                pass
            def bar():
                pass
        """)
        tree = ast.parse(source)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        assert functions == ["foo", "bar"]

    def test_compile_and_exec(self) -> None:
        """Compiled AST can be executed."""
        source = "result = 2 ** 10"
        code = compile(source, "<string>", "exec")
        namespace: dict = {}
        exec(code, namespace)
        assert namespace["result"] == 1024
