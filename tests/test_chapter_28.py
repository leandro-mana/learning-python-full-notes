"""Tests for Chapter 28: Command-Line Interfaces."""

import argparse
import os
import sys


class TestArgparseFundamentals:
    """Test argparse basics."""

    def test_positional_argument(self) -> None:
        """Positional arguments are required by default."""
        parser = argparse.ArgumentParser()
        parser.add_argument("name")
        args = parser.parse_args(["Alice"])
        assert args.name == "Alice"

    def test_optional_argument(self) -> None:
        """Optional arguments use -- prefix."""
        parser = argparse.ArgumentParser()
        parser.add_argument("--verbose", action="store_true")
        parser.add_argument("--count", type=int, default=1)

        args = parser.parse_args(["--verbose", "--count", "5"])
        assert args.verbose is True
        assert args.count == 5

    def test_default_values(self) -> None:
        """Arguments have configurable defaults."""
        parser = argparse.ArgumentParser()
        parser.add_argument("--output", default="stdout")
        args = parser.parse_args([])
        assert args.output == "stdout"

    def test_choices_restrict_values(self) -> None:
        """choices limits accepted values."""
        parser = argparse.ArgumentParser()
        parser.add_argument("--level", choices=["debug", "info", "warning"])

        args = parser.parse_args(["--level", "info"])
        assert args.level == "info"

    def test_nargs_multiple_values(self) -> None:
        """nargs accepts multiple values for an argument."""
        parser = argparse.ArgumentParser()
        parser.add_argument("files", nargs="+")
        args = parser.parse_args(["a.txt", "b.txt", "c.txt"])
        assert args.files == ["a.txt", "b.txt", "c.txt"]

    def test_short_and_long_flags(self) -> None:
        """Arguments can have short and long forms."""
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", action="store_true")
        args = parser.parse_args(["-v"])
        assert args.verbose is True


class TestSubcommands:
    """Test argparse subcommands."""

    def test_subparsers(self) -> None:
        """Subparsers create git-style subcommands."""
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command")

        init_parser = sub.add_parser("init")
        init_parser.add_argument("--bare", action="store_true")

        clone_parser = sub.add_parser("clone")
        clone_parser.add_argument("url")

        args = parser.parse_args(["clone", "https://example.com/repo"])
        assert args.command == "clone"
        assert args.url == "https://example.com/repo"

    def test_mutually_exclusive_group(self) -> None:
        """Mutually exclusive groups prevent conflicting options."""
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--json", action="store_true")
        group.add_argument("--csv", action="store_true")

        args = parser.parse_args(["--json"])
        assert args.json is True
        assert args.csv is False


class TestEnvironmentAndConfig:
    """Test environment variables and sys module."""

    def test_environ_access(self) -> None:
        """os.environ provides access to environment variables."""
        os.environ["TEST_VAR_CH28"] = "hello"
        assert os.environ["TEST_VAR_CH28"] == "hello"
        del os.environ["TEST_VAR_CH28"]

    def test_environ_get_default(self) -> None:
        """environ.get returns a default for missing variables."""
        result = os.environ.get("NONEXISTENT_VAR_CH28", "fallback")
        assert result == "fallback"

    def test_sys_argv_is_list(self) -> None:
        """sys.argv is a list of command-line arguments."""
        assert isinstance(sys.argv, list)
        assert len(sys.argv) >= 1

    def test_sys_exit_raises_systemexit(self) -> None:
        """sys.exit raises SystemExit exception."""
        try:
            sys.exit(1)
        except SystemExit as e:
            assert e.code == 1
