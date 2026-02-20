"""Tests for Chapter 8: File I/O and Data Serialization."""

import csv
import json
from pathlib import Path


class TestFileOperations:
    """Test core file I/O."""

    def test_write_and_read_text(self, tmp_path: Path) -> None:
        """Write and read text files."""
        filepath = tmp_path / "test.txt"
        filepath.write_text("Hello, World!", encoding="utf-8")

        content = filepath.read_text(encoding="utf-8")
        assert content == "Hello, World!"

    def test_write_and_read_lines(self, tmp_path: Path) -> None:
        """Write and read multiple lines."""
        filepath = tmp_path / "lines.txt"
        lines = ["line 1\n", "line 2\n", "line 3\n"]

        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)

        with open(filepath, encoding="utf-8") as f:
            read_lines = f.readlines()

        assert read_lines == lines

    def test_context_manager_closes_file(self, tmp_path: Path) -> None:
        """Context manager ensures file is closed."""
        filepath = tmp_path / "test.txt"
        filepath.write_text("test", encoding="utf-8")

        with open(filepath, encoding="utf-8") as f:
            _ = f.read()

        assert f.closed

    def test_binary_mode(self, tmp_path: Path) -> None:
        """Binary mode reads/writes bytes."""
        filepath = tmp_path / "binary.dat"
        data = b"\x00\x01\x02\x03"

        filepath.write_bytes(data)
        content = filepath.read_bytes()
        assert content == data


class TestPathlib:
    """Test pathlib operations."""

    def test_path_construction(self) -> None:
        """Paths can be constructed with / operator."""
        base = Path("/usr") / "local" / "bin"
        assert str(base) == "/usr/local/bin"

    def test_path_parts(self) -> None:
        """Path components are accessible."""
        p = Path("/home/user/project/main.py")
        assert p.name == "main.py"
        assert p.stem == "main"
        assert p.suffix == ".py"
        assert p.parent == Path("/home/user/project")

    def test_glob_pattern(self, tmp_path: Path) -> None:
        """glob finds files matching patterns."""
        (tmp_path / "a.py").touch()
        (tmp_path / "b.py").touch()
        (tmp_path / "c.txt").touch()

        py_files = sorted(tmp_path.glob("*.py"))
        assert len(py_files) == 2

    def test_mkdir_parents(self, tmp_path: Path) -> None:
        """mkdir with parents creates nested directories."""
        nested = tmp_path / "a" / "b" / "c"
        nested.mkdir(parents=True)
        assert nested.is_dir()


class TestDataSerialization:
    """Test JSON, CSV serialization."""

    def test_json_roundtrip(self) -> None:
        """JSON serialize and deserialize."""
        data = {"name": "Alice", "scores": [95, 87, 92], "active": True}
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        assert parsed == data

    def test_json_pretty_print(self) -> None:
        """JSON with indentation for readability."""
        data = {"key": "value"}
        pretty = json.dumps(data, indent=2)
        assert "\n" in pretty
        assert "  " in pretty

    def test_csv_dictreader_writer(self, tmp_path: Path) -> None:
        """CSV DictReader/DictWriter roundtrip."""
        filepath = tmp_path / "data.csv"
        rows = [
            {"name": "Alice", "age": "30"},
            {"name": "Bob", "age": "25"},
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "age"])
            writer.writeheader()
            writer.writerows(rows)

        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            read_rows = list(reader)

        assert read_rows == rows

    def test_json_file_roundtrip(self, tmp_path: Path) -> None:
        """JSON file read/write roundtrip."""
        filepath = tmp_path / "config.json"
        config = {"host": "localhost", "port": 8080}

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(config, f)

        with open(filepath, encoding="utf-8") as f:
            loaded = json.load(f)

        assert loaded == config
