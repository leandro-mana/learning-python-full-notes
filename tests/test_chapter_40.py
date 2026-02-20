"""Tests for Chapter 40: Import System Internals."""

import importlib
import importlib.metadata
import pkgutil
import sys
import types


class TestImportlibBasics:
    """Test importlib core functionality."""

    def test_import_module(self) -> None:
        """importlib.import_module imports by string name."""
        math = importlib.import_module("math")
        assert math.pi == __import__("math").pi

    def test_import_submodule(self) -> None:
        """importlib can import submodules."""
        path_mod = importlib.import_module("os.path")
        assert hasattr(path_mod, "join")

    def test_reload_module(self) -> None:
        """importlib.reload re-imports a module."""
        import json

        reloaded = importlib.reload(json)
        assert reloaded is json

    def test_module_has_spec(self) -> None:
        """Modules have a __spec__ attribute."""
        import json

        assert json.__spec__ is not None
        assert json.__spec__.name == "json"

    def test_module_attributes(self) -> None:
        """Modules have standard attributes."""
        import json

        assert hasattr(json, "__name__")
        assert hasattr(json, "__file__")
        assert hasattr(json, "__package__")
        assert json.__name__ == "json"


class TestImportHooks:
    """Test import system hooks and finders."""

    def test_sys_meta_path(self) -> None:
        """sys.meta_path contains finder objects."""
        assert len(sys.meta_path) > 0
        for finder in sys.meta_path:
            assert hasattr(finder, "find_module") or hasattr(finder, "find_spec")

    def test_sys_path_is_list(self) -> None:
        """sys.path is a list of directory strings."""
        assert isinstance(sys.path, list)
        assert len(sys.path) > 0

    def test_find_spec(self) -> None:
        """importlib.util.find_spec locates modules."""
        spec = importlib.util.find_spec("json")
        assert spec is not None
        assert spec.name == "json"
        assert spec.origin is not None

    def test_find_spec_nonexistent(self) -> None:
        """find_spec returns None for missing modules."""
        spec = importlib.util.find_spec("nonexistent_module_xyz_123")
        assert spec is None

    def test_create_module_from_spec(self) -> None:
        """Modules can be created from specs."""
        spec = importlib.util.find_spec("json")
        assert spec is not None
        assert spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        assert isinstance(module, types.ModuleType)
        assert module.__name__ == "json"

    def test_sys_modules_cache(self) -> None:
        """sys.modules caches imported modules."""
        import json

        assert "json" in sys.modules
        assert sys.modules["json"] is json


class TestPackageUtilities:
    """Test pkgutil and importlib.metadata."""

    def test_pkgutil_iter_modules(self) -> None:
        """pkgutil.iter_modules lists available modules."""
        modules = list(pkgutil.iter_modules())
        assert len(modules) > 0

    def test_pkgutil_module_info(self) -> None:
        """Module info includes name and ispkg flag."""
        for info in pkgutil.iter_modules():
            assert hasattr(info, "name")
            assert hasattr(info, "ispkg")
            break  # Just check first one

    def test_importlib_metadata_version(self) -> None:
        """importlib.metadata.version returns package version."""
        version = importlib.metadata.version("pip")
        assert isinstance(version, str)
        assert len(version) > 0

    def test_importlib_metadata_packages(self) -> None:
        """importlib.metadata.packages_distributions maps packages."""
        distributions = importlib.metadata.packages_distributions()
        assert isinstance(distributions, dict)
        assert len(distributions) > 0

    def test_importlib_metadata_not_found(self) -> None:
        """Missing packages raise PackageNotFoundError."""
        try:
            importlib.metadata.version("nonexistent_package_xyz_123")
            assert False, "Should have raised"
        except importlib.metadata.PackageNotFoundError:
            pass

    def test_module_is_package(self) -> None:
        """Packages have __path__ attribute, modules don't."""
        import email
        import math

        assert hasattr(email, "__path__")  # email is a package
        assert not hasattr(math, "__path__")  # math is a builtin module

    def test_sys_builtin_module_names(self) -> None:
        """sys.builtin_module_names lists C-builtin modules."""
        assert "sys" in sys.builtin_module_names
        assert isinstance(sys.builtin_module_names, tuple)
