"""Tests for Chapter 41: Concurrency Patterns."""

import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from queue import Empty, Queue


class TestThreadingSynchronization:
    """Test threading synchronization primitives."""

    def test_lock_mutual_exclusion(self) -> None:
        """Lock ensures mutual exclusion."""
        lock = threading.Lock()
        counter = [0]

        def increment() -> None:
            for _ in range(1000):
                with lock:
                    counter[0] += 1

        threads = [threading.Thread(target=increment) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert counter[0] == 4000

    def test_rlock_reentrant(self) -> None:
        """RLock allows reentrant locking."""
        lock = threading.RLock()
        with lock:
            with lock:  # Would deadlock with regular Lock
                acquired = True
        assert acquired

    def test_event_signaling(self) -> None:
        """Event signals between threads."""
        event = threading.Event()
        result: list[str] = []

        def waiter() -> None:
            event.wait(timeout=5)
            result.append("done")

        t = threading.Thread(target=waiter)
        t.start()
        event.set()
        t.join()
        assert result == ["done"]

    def test_semaphore_limits_access(self) -> None:
        """Semaphore limits concurrent access."""
        sem = threading.Semaphore(2)
        max_concurrent = [0]
        current = [0]
        lock = threading.Lock()

        def worker() -> None:
            with sem:
                with lock:
                    current[0] += 1
                    if current[0] > max_concurrent[0]:
                        max_concurrent[0] = current[0]
                time.sleep(0.01)
                with lock:
                    current[0] -= 1

        threads = [threading.Thread(target=worker) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert max_concurrent[0] <= 2

    def test_barrier(self) -> None:
        """Barrier synchronizes a fixed number of threads."""
        barrier = threading.Barrier(3)
        arrivals: list[int] = []
        lock = threading.Lock()

        def worker(worker_id: int) -> None:
            barrier.wait()
            with lock:
                arrivals.append(worker_id)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(arrivals) == 3


class TestConcurrentFutures:
    """Test concurrent.futures high-level API."""

    def test_thread_pool_submit(self) -> None:
        """ThreadPoolExecutor.submit returns a Future."""
        with ThreadPoolExecutor(max_workers=2) as pool:
            future = pool.submit(lambda x: x**2, 5)
            assert isinstance(future, Future)
            assert future.result() == 25

    def test_thread_pool_map(self) -> None:
        """ThreadPoolExecutor.map applies function to iterables."""
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda x: x * 2, [1, 2, 3, 4]))
        assert results == [2, 4, 6, 8]

    def test_as_completed(self) -> None:
        """as_completed yields futures as they finish."""
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = {pool.submit(lambda x: x**2, i): i for i in range(5)}
            results: list[int] = []
            for future in as_completed(futures):
                results.append(future.result())
        assert sorted(results) == [0, 1, 4, 9, 16]

    def test_future_exception(self) -> None:
        """Future captures exceptions from workers."""

        def failing() -> None:
            raise ValueError("task failed")

        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(failing)
            assert future.exception() is not None
            assert isinstance(future.exception(), ValueError)

    def test_future_done_and_cancel(self) -> None:
        """Futures report completion status."""
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(lambda: 42)
            result = future.result()
            assert result == 42
            assert future.done()


class TestThreadSafePatterns:
    """Test thread-safe data patterns."""

    def test_queue_basic(self) -> None:
        """Queue provides thread-safe FIFO."""
        q: Queue[int] = Queue()
        q.put(1)
        q.put(2)
        assert q.get() == 1
        assert q.get() == 2

    def test_queue_producer_consumer(self) -> None:
        """Producer-consumer pattern with Queue."""
        q: Queue[int | None] = Queue()
        results: list[int] = []
        lock = threading.Lock()

        def producer() -> None:
            for i in range(5):
                q.put(i)
            q.put(None)  # Sentinel

        def consumer() -> None:
            while True:
                item = q.get()
                if item is None:
                    break
                with lock:
                    results.append(item)

        t1 = threading.Thread(target=producer)
        t2 = threading.Thread(target=consumer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        assert sorted(results) == [0, 1, 2, 3, 4]

    def test_queue_timeout(self) -> None:
        """Queue.get raises Empty on timeout."""
        q: Queue[int] = Queue()
        try:
            q.get(timeout=0.01)
            assert False, "Should have raised"
        except Empty:
            pass

    def test_thread_local_storage(self) -> None:
        """threading.local provides per-thread storage."""
        local = threading.local()
        results: list[int] = []
        lock = threading.Lock()

        def worker(value: int) -> None:
            local.data = value
            time.sleep(0.01)
            with lock:
                results.append(local.data)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert sorted(results) == [0, 1, 2, 3]

    def test_queue_maxsize(self) -> None:
        """Queue can limit its size."""
        q: Queue[int] = Queue(maxsize=2)
        q.put(1)
        q.put(2)
        assert q.full()
        assert q.qsize() == 2
