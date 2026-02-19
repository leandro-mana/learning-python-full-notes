# Chapter 5: Decorators, Generators, and Context Managers

Function and class decorators, generator functions and expressions, and context managers. Essential tools for clean, Pythonic code.

## Overview

Decorators enable aspect-oriented programming and metaprogramming. Generators provide lazy evaluation for memory-efficient iteration. Context managers ensure proper resource cleanup. Together, these are hallmarks of idiomatic Python.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_05/
```

| Notebook | Topics |
| --- | --- |
| **01_decorators.ipynb** | Function decorators, `@wraps`, parameterized decorators, class decorators, stacking, practical patterns (memoization, timing, retry) |
| **02_generators_and_yield.ipynb** | Generator functions, `yield`, generator expressions, `send()`, `yield from`, lazy pipelines |
| **03_context_managers.ipynb** | `with` statement, `__enter__`/`__exit__`, `@contextmanager`, nested contexts, async context managers |

## Key Concepts

### Basic Function Decorators

```python
from functools import wraps
from typing import Callable, Any

def simple_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Before calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After calling {func.__name__}")
        return result
    return wrapper

@simple_decorator
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### Parameterized Decorators

```python
def repeat(times: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> list[Any]:
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator

@repeat(times=3)
def echo(message: str) -> str:
    return message

result = echo("Hi")  # ["Hi", "Hi", "Hi"]
```

### Generator Functions

```python
from typing import Generator

def fibonacci() -> Generator[int, None, None]:
    """Infinite Fibonacci sequence - lazy evaluation."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from itertools import islice
first_10 = list(islice(fibonacci(), 10))
```

### Context Managers

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label: str):
    """Context manager that times a block of code."""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed:.4f}s")

with timer("Processing"):
    pass  # ... do work ...
```

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_05.py -v
```

## References

- Learning Python, 5th Edition - Part IV: Functions and Generators
- PEP 318 - Decorators for Functions and Methods
- PEP 343 - The "with" Statement
- [functools documentation](https://docs.python.org/3/library/functools.html)
- [contextlib documentation](https://docs.python.org/3/library/contextlib.html)
