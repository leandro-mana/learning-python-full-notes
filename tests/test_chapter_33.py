"""Tests for Chapter 33: OS and System Interaction."""

import os
import platform
import shutil
import subprocess
import sys
import tempfile


class TestOSAndPlatform:
    """Test os and platform modules."""

    def test_os_getcwd(self) -> None:
        """os.getcwd returns current working directory."""
        cwd = os.getcwd()
        assert isinstance(cwd, str)
        assert os.path.isdir(cwd)

    def test_os_path_operations(self) -> None:
        """os.path provides path manipulation."""
        path = os.path.join("src", "chapter_33", "__init__.py")
        assert os.path.basename(path) == "__init__.py"
        assert os.path.dirname(path) == os.path.join("src", "chapter_33")
        name, ext = os.path.splitext("script.py")
        assert name == "script"
        assert ext == ".py"

    def test_os_environ_is_mapping(self) -> None:
        """os.environ is a mapping of environment variables."""
        assert isinstance(os.environ, os.environ.__class__)
        assert "PATH" in os.environ

    def test_platform_info(self) -> None:
        """platform module provides system information."""
        assert platform.system() in ("Darwin", "Linux", "Windows")
        assert isinstance(platform.python_version(), str)
        assert (
            platform.python_version()
            == f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )

    def test_os_walk(self) -> None:
        """os.walk traverses directory trees."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, "sub"))
            open(os.path.join(tmpdir, "file.txt"), "w").close()
            open(os.path.join(tmpdir, "sub", "nested.txt"), "w").close()

            dirs_found: list[str] = []
            for dirpath, dirnames, filenames in os.walk(tmpdir):
                dirs_found.append(dirpath)
            assert len(dirs_found) == 2


class TestShutilAndTempfile:
    """Test shutil and tempfile operations."""

    def test_shutil_copy(self) -> None:
        """shutil.copy copies files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "source.txt")
            dst = os.path.join(tmpdir, "dest.txt")
            with open(src, "w") as f:
                f.write("hello")
            shutil.copy(src, dst)
            with open(dst) as f:
                assert f.read() == "hello"

    def test_shutil_copytree(self) -> None:
        """shutil.copytree copies directory trees."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = os.path.join(tmpdir, "src")
            dst_dir = os.path.join(tmpdir, "dst")
            os.makedirs(src_dir)
            with open(os.path.join(src_dir, "file.txt"), "w") as f:
                f.write("content")
            shutil.copytree(src_dir, dst_dir)
            assert os.path.exists(os.path.join(dst_dir, "file.txt"))

    def test_shutil_disk_usage(self) -> None:
        """shutil.disk_usage returns disk space info."""
        usage = shutil.disk_usage("/")
        assert usage.total > 0
        assert usage.used > 0
        assert usage.free > 0

    def test_tempfile_named(self) -> None:
        """NamedTemporaryFile creates a temporary file with a name."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("temp data")
            name = f.name
        assert os.path.exists(name)
        os.unlink(name)

    def test_tempfile_directory(self) -> None:
        """TemporaryDirectory auto-cleans on exit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            assert os.path.isdir(tmpdir)
            path = tmpdir
        assert not os.path.exists(path)


class TestSubprocess:
    """Test subprocess module."""

    def test_subprocess_run(self) -> None:
        """subprocess.run executes a command."""
        result = subprocess.run(["echo", "hello"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_subprocess_capture_stderr(self) -> None:
        """subprocess captures stderr separately."""
        result = subprocess.run(
            [sys.executable, "-c", "import sys; sys.stderr.write('error\\n')"],
            capture_output=True,
            text=True,
        )
        assert "error" in result.stderr

    def test_subprocess_check_returncode(self) -> None:
        """check_returncode raises on non-zero exit."""
        result = subprocess.run(
            [sys.executable, "-c", "raise SystemExit(1)"],
            capture_output=True,
        )
        assert result.returncode == 1
        try:
            result.check_returncode()
            assert False, "Should have raised"
        except subprocess.CalledProcessError:
            pass

    def test_subprocess_pipe(self) -> None:
        """subprocess can pipe between commands."""
        result = subprocess.run(
            [sys.executable, "-c", "print('hello world')"],
            capture_output=True,
            text=True,
        )
        assert result.stdout.strip() == "hello world"
