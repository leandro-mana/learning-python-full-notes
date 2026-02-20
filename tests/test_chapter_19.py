"""Tests for Chapter 19: Packaging and Distribution."""

import importlib.metadata
import sys
import sysconfig
import venv
from pathlib import Path


class TestVirtualEnvironments:
    """Test virtual environment concepts."""

    def test_sys_prefix_identifies_environment(self) -> None:
        """sys.prefix points to the active environment."""
        assert Path(sys.prefix).exists()
        assert Path(sys.executable).exists()

    def test_venv_builder_exists(self) -> None:
        """venv module provides EnvBuilder for creating environments."""
        builder = venv.EnvBuilder(with_pip=False)
        assert hasattr(builder, "create")

    def test_sysconfig_paths(self) -> None:
        """sysconfig provides installation paths."""
        paths = sysconfig.get_paths()
        assert "purelib" in paths
        assert "scripts" in paths
        assert "include" in paths


class TestPackageMetadata:
    """Test package metadata access."""

    def test_installed_package_version(self) -> None:
        """importlib.metadata reads installed package info."""
        version = importlib.metadata.version("pip")
        assert version is not None
        parts = version.split(".")
        assert len(parts) >= 2  # Major.minor at minimum

    def test_package_metadata_fields(self) -> None:
        """Package metadata contains standard fields."""
        meta = importlib.metadata.metadata("pip")
        assert meta["Name"] == "pip"
        assert "Version" in meta
        assert "Summary" in meta

    def test_entry_points(self) -> None:
        """Entry points expose console scripts and plugins."""
        eps = importlib.metadata.entry_points()
        # entry_points() returns a SelectableGroups or dict-like
        assert eps is not None


class TestVersionParsing:
    """Test version string handling."""

    def test_version_comparison(self) -> None:
        """Version strings can be compared with packaging conventions."""
        from importlib.metadata import version

        pip_version = version("pip")
        # Version string is parseable
        parts = pip_version.split(".")
        major = int(parts[0])
        assert major >= 1

    def test_python_version(self) -> None:
        """sys.version_info provides structured version info."""
        assert sys.version_info.major == 3
        assert sys.version_info.minor >= 12
        assert isinstance(sys.version_info.releaselevel, str)
