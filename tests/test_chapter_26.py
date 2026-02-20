"""Tests for Chapter 26: Async Programming."""

import asyncio


class TestCoroutineBasics:
    """Test coroutine fundamentals."""

    def test_coroutine_is_awaitable(self) -> None:
        """Coroutines are awaitable objects."""

        async def greet() -> str:
            return "hello"

        coro = greet()
        assert asyncio.iscoroutine(coro)
        result = asyncio.run(coro)
        assert result == "hello"

    def test_await_chains_coroutines(self) -> None:
        """await passes control between coroutines."""

        async def add(a: int, b: int) -> int:
            return a + b

        async def main() -> int:
            result = await add(3, 4)
            return result

        assert asyncio.run(main()) == 7

    def test_async_sleep(self) -> None:
        """asyncio.sleep yields control to the event loop."""

        async def delayed_value() -> str:
            await asyncio.sleep(0)
            return "done"

        assert asyncio.run(delayed_value()) == "done"


class TestTasksAndGather:
    """Test task creation and gathering."""

    def test_gather_runs_concurrently(self) -> None:
        """asyncio.gather runs coroutines concurrently."""
        results: list[int] = []

        async def append_value(val: int) -> int:
            await asyncio.sleep(0)
            results.append(val)
            return val

        async def main() -> list[int]:
            return await asyncio.gather(
                append_value(1),
                append_value(2),
                append_value(3),
            )

        gathered = asyncio.run(main())
        assert gathered == [1, 2, 3]
        assert sorted(results) == [1, 2, 3]

    def test_create_task_schedules(self) -> None:
        """create_task schedules a coroutine for execution."""

        async def compute(x: int) -> int:
            await asyncio.sleep(0)
            return x * 2

        async def main() -> int:
            task = asyncio.create_task(compute(5))
            result = await task
            return result

        assert asyncio.run(main()) == 10

    def test_gather_preserves_order(self) -> None:
        """gather returns results in argument order, not completion order."""

        async def delayed(val: int, delay: float) -> int:
            await asyncio.sleep(delay)
            return val

        async def main() -> list[int]:
            return await asyncio.gather(
                delayed(1, 0.02),
                delayed(2, 0.01),
                delayed(3, 0.0),
            )

        assert asyncio.run(main()) == [1, 2, 3]


class TestAsyncPatterns:
    """Test async iteration and context managers."""

    def test_async_iterator(self) -> None:
        """Async iterators use __aiter__ and __anext__."""

        class AsyncRange:
            def __init__(self, stop: int) -> None:
                self.stop = stop
                self.current = 0

            def __aiter__(self):
                return self

            async def __anext__(self) -> int:
                if self.current >= self.stop:
                    raise StopAsyncIteration
                value = self.current
                self.current += 1
                return value

        async def collect() -> list[int]:
            return [i async for i in AsyncRange(4)]

        assert asyncio.run(collect()) == [0, 1, 2, 3]

    def test_async_generator(self) -> None:
        """Async generators use yield in async functions."""

        async def async_range(stop: int):
            for i in range(stop):
                await asyncio.sleep(0)
                yield i

        async def collect() -> list[int]:
            return [i async for i in async_range(3)]

        assert asyncio.run(collect()) == [0, 1, 2]

    def test_async_context_manager(self) -> None:
        """Async context managers use __aenter__ and __aexit__."""
        events: list[str] = []

        class AsyncResource:
            async def __aenter__(self):
                events.append("enter")
                return self

            async def __aexit__(self, *args: object) -> None:
                events.append("exit")

        async def main() -> None:
            async with AsyncResource():
                events.append("use")

        asyncio.run(main())
        assert events == ["enter", "use", "exit"]

    def test_semaphore_limits_concurrency(self) -> None:
        """Semaphores limit the number of concurrent operations."""
        max_concurrent = 0
        current = 0

        async def limited_task(sem: asyncio.Semaphore) -> None:
            nonlocal max_concurrent, current
            async with sem:
                current += 1
                if current > max_concurrent:
                    max_concurrent = current
                await asyncio.sleep(0.01)
                current -= 1

        async def main() -> int:
            sem = asyncio.Semaphore(2)
            await asyncio.gather(*(limited_task(sem) for _ in range(5)))
            return max_concurrent

        result = asyncio.run(main())
        assert result <= 2
