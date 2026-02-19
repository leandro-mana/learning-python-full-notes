"""Tests for Chapter 7: Modules and Packages."""

import importlib
import sys
from types import ModuleType


class TestModuleBasics:
    """Test module fundamentals."""

    def test_import_creates_module_object(self) -> None:
        """Importing a module creates a module object."""
        import json

        assert isinstance(json, ModuleType)
        assert hasattr(json, "dumps")
        assert hasattr(json, "loads")

    def test_module_has_name(self) -> None:
        """Modules have a __name__ attribute."""
        import os

        assert os.__name__ == "os"

    def test_module_in_sys_modules(self) -> None:
        """Imported modules are cached in sys.modules."""
        import json

        assert "json" in sys.modules
        assert sys.modules["json"] is json

    def test_dir_lists_module_attributes(self) -> None:
        """dir() lists module attributes."""
        import math

        attrs = dir(math)
        assert "pi" in attrs
        assert "sqrt" in attrs
        assert "ceil" in attrs


class TestImportMechanisms:
    """Test different import patterns."""

    def test_from_import(self) -> None:
        """from ... import brings specific names into scope."""
        from math import pi, sqrt

        assert isinstance(pi, float)
        assert sqrt(16) == 4.0

    def test_import_as_alias(self) -> None:
        """import ... as creates an alias."""
        import collections as col

        assert col.Counter is __import__("collections").Counter

    def test_importlib_import_module(self) -> None:
        """importlib.import_module for dynamic imports."""
        mod = importlib.import_module("json")
        assert hasattr(mod, "dumps")
        assert mod.__name__ == "json"


class TestPackageStructure:
    """Test package concepts."""

    def test_package_has_path(self) -> None:
        """Packages have __path__ attribute, modules don't."""
        import email

        # email is a package (has __path__)
        assert hasattr(email, "__path__")
        # json is a module (no __path__)
        # Note: in some Python versions json is a package too

    def test_sys_path_is_list(self) -> None:
        """sys.path is a list of strings for module search."""
        assert isinstance(sys.path, list)
        assert all(isinstance(p, str) for p in sys.path)

    def test_conditional_import_pattern(self) -> None:
        """Conditional imports handle optional dependencies."""
        try:
            importlib.import_module("nonexistent_module")
            has_module = True
        except ImportError:
            has_module = False

        assert has_module is False
