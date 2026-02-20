"""Tests for Chapter 27: Multiprocessing and Parallelism."""

import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor


def _square(x: int) -> int:
    """Square a number (module-level for pickling)."""
    return x * x


def _get_pid(_: int = 0) -> int:
    """Return current process ID (module-level for pickling)."""
    return os.getpid()


def _queue_worker(q: multiprocessing.Queue) -> None:
    """Put a value into a queue (module-level for pickling)."""
    q.put(42)


class TestMultiprocessingBasics:
    """Test multiprocessing fundamentals."""

    def test_process_runs_function(self) -> None:
        """Process executes a target function."""
        result: multiprocessing.Queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=_queue_worker, args=(result,))
        p.start()
        p.join()
        assert result.get() == 42

    def test_pool_map(self) -> None:
        """Pool.map applies a function across inputs in parallel."""
        with multiprocessing.Pool(2) as pool:
            results = pool.map(_square, [1, 2, 3, 4])
        assert results == [1, 4, 9, 16]

    def test_separate_process_ids(self) -> None:
        """Each process has its own PID."""
        with multiprocessing.Pool(2) as pool:
            pids = pool.map(_get_pid, range(4))
        # At least one worker PID differs from the main process
        assert any(pid != os.getpid() for pid in pids)


class TestSharedStateAndIPC:
    """Test inter-process communication."""

    def test_queue_communication(self) -> None:
        """Queue enables safe inter-process communication."""
        q: multiprocessing.Queue = multiprocessing.Queue()
        q.put("hello")
        q.put("world")
        assert q.get() == "hello"
        assert q.get() == "world"

    def test_value_shared_state(self) -> None:
        """Value provides shared state between processes."""
        counter = multiprocessing.Value("i", 0)
        assert counter.value == 0
        counter.value = 42
        assert counter.value == 42

    def test_array_shared_state(self) -> None:
        """Array provides shared array between processes."""
        arr = multiprocessing.Array("d", [1.0, 2.0, 3.0])
        assert list(arr) == [1.0, 2.0, 3.0]
        arr[0] = 10.0
        assert arr[0] == 10.0

    def test_pipe_bidirectional(self) -> None:
        """Pipe provides bidirectional communication."""
        parent_conn, child_conn = multiprocessing.Pipe()
        parent_conn.send("ping")
        assert child_conn.recv() == "ping"
        child_conn.send("pong")
        assert parent_conn.recv() == "pong"


class TestProcessPoolExecutor:
    """Test concurrent.futures with processes."""

    def test_executor_map(self) -> None:
        """ProcessPoolExecutor.map distributes work across processes."""
        with ProcessPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(_square, [1, 2, 3, 4, 5]))
        assert results == [1, 4, 9, 16, 25]

    def test_executor_submit_future(self) -> None:
        """submit returns a Future with the result."""
        with ProcessPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_square, 7)
            assert future.result() == 49

    def test_cpu_count(self) -> None:
        """os.cpu_count returns the number of CPUs."""
        cpus = os.cpu_count()
        assert cpus is not None
        assert cpus >= 1
