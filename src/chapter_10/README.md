# Chapter 10: Concurrency, Testing, and Best Practices

Async/await, threading, testing with pytest, debugging, profiling, and production-ready Python patterns.

## Overview

This chapter covers the advanced topics that round out a senior Python developer's toolkit: concurrency models (threads, processes, asyncio), professional testing with pytest, and debugging/profiling techniques for production code.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_10/
```

| Notebook | Topics |
| --- | --- |
| **01_concurrency_basics.ipynb** | Threading, GIL, locks, concurrent.futures, async/await, threads vs processes vs asyncio |
| **02_testing_with_pytest.ipynb** | Fixtures, parametrize, markers, mocking, assertion patterns, AAA pattern |
| **03_debugging_and_profiling.ipynb** | logging, pdb, assert, timeit, cProfile, memory optimization, performance patterns |

## Key Concepts

### concurrent.futures

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch(url: str) -> str:
    ...

with ThreadPoolExecutor(max_workers=5) as pool:
    futures = {pool.submit(fetch, url): url for url in urls}
    for future in as_completed(futures):
        result = future.result()
```

### pytest Fixtures and Parametrize

```python
import pytest

@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

@pytest.mark.parametrize("input,expected", [(1, 1), (2, 4), (3, 9)])
def test_square(input: int, expected: int) -> None:
    assert input ** 2 == expected
```

### Profiling

```python
import cProfile

cProfile.run("my_function()", sort="cumulative")
```

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_10.py -v
```

## References

- Learning Python, 5th Edition - Part VIII: Advanced Topics
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [pytest documentation](https://docs.pytest.org/)
- [cProfile documentation](https://docs.python.org/3/library/profile.html)
