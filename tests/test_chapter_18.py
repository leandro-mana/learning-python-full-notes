"""Tests for Chapter 18: Database Access."""

import sqlite3


class TestSQLiteFundamentals:
    """Test sqlite3 basics."""

    def test_create_and_query(self) -> None:
        """Create a table and query it."""
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
        conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 25))

        rows = conn.execute("SELECT name, age FROM users ORDER BY name").fetchall()
        assert rows == [("Alice", 30), ("Bob", 25)]
        conn.close()

    def test_parameterized_queries(self) -> None:
        """Parameterized queries prevent SQL injection."""
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO items (name) VALUES (?)", ("Widget",))

        # Parameterized query safely handles special characters
        malicious = "'; DROP TABLE items; --"
        conn.execute("INSERT INTO items (name) VALUES (?)", (malicious,))
        rows = conn.execute("SELECT name FROM items").fetchall()
        assert len(rows) == 2  # Table still exists with both rows

        conn.close()

    def test_executemany_batch_insert(self) -> None:
        """executemany efficiently inserts multiple rows."""
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE numbers (value INTEGER)")

        data = [(i,) for i in range(100)]
        conn.executemany("INSERT INTO numbers (value) VALUES (?)", data)

        count = conn.execute("SELECT COUNT(*) FROM numbers").fetchone()[0]
        assert count == 100
        conn.close()


class TestTransactions:
    """Test transaction handling."""

    def test_commit_persists_data(self) -> None:
        """Committed data persists."""
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE t (val TEXT)")
        conn.execute("INSERT INTO t (val) VALUES (?)", ("kept",))
        conn.commit()

        rows = conn.execute("SELECT val FROM t").fetchall()
        assert rows == [("kept",)]
        conn.close()

    def test_rollback_discards_changes(self) -> None:
        """Rollback discards uncommitted changes."""
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE t (val TEXT)")
        conn.execute("INSERT INTO t (val) VALUES (?)", ("initial",))
        conn.commit()

        conn.execute("INSERT INTO t (val) VALUES (?)", ("discarded",))
        conn.rollback()

        rows = conn.execute("SELECT val FROM t").fetchall()
        assert rows == [("initial",)]
        conn.close()

    def test_context_manager_auto_commit(self) -> None:
        """Connection as context manager auto-commits on success."""
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE t (val TEXT)")

        with conn:
            conn.execute("INSERT INTO t (val) VALUES (?)", ("auto-committed",))

        rows = conn.execute("SELECT val FROM t").fetchall()
        assert rows == [("auto-committed",)]
        conn.close()


class TestRowFactories:
    """Test custom row factories."""

    def test_row_factory_dict(self) -> None:
        """sqlite3.Row provides dict-like access."""
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))

        row = conn.execute("SELECT * FROM users").fetchone()
        assert row["name"] == "Alice"
        assert row["age"] == 30
        assert list(row.keys()) == ["id", "name", "age"]
        conn.close()

    def test_custom_row_factory(self) -> None:
        """Custom row factories transform query results."""
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE points (x REAL, y REAL)")
        conn.execute("INSERT INTO points (x, y) VALUES (?, ?)", (1.0, 2.0))
        conn.execute("INSERT INTO points (x, y) VALUES (?, ?)", (3.0, 4.0))

        def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict:
            return {col[0]: value for col, value in zip(cursor.description, row)}

        conn.row_factory = dict_factory
        rows = conn.execute("SELECT x, y FROM points ORDER BY x").fetchall()
        assert rows == [{"x": 1.0, "y": 2.0}, {"x": 3.0, "y": 4.0}]
        conn.close()
