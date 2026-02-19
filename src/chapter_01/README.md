# Chapter 1: Getting Started - Python Fundamentals

Core Python concepts through professional patterns and idioms. Focus on type safety, best practices, and production-ready code.

## Overview

Python fundamentals reviewed through the lens of industry best practices: proper use of data types, control flow patterns, function design, and code organization that scales to large codebases.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_01/
```

| Notebook | Topics |
| --- | --- |
| **01_core_concepts.ipynb** | Data types, mutability, operators, truthiness, identity vs equality |
| **02_control_structures.ipynb** | if/else, loops, comprehensions, match/case, exception handling |
| **03_functional_programming.ipynb** | First-class functions, closures, higher-order functions, lambda, map/filter/reduce |
| **04_strings_and_unicode.ipynb** | String methods, f-strings, encoding/decoding, Unicode handling |
| **05_type_hints_intro.ipynb** | Type annotations, typing module, mypy basics |

## Key Concepts

### Data Types and Mutability

```python
# Immutable types: int, float, str, tuple, frozenset
x: int = 42
greeting: str = "Hello"
coords: tuple[int, int] = (10, 20)

# Mutable types: list, dict, set
items: list[str] = ["a", "b"]
config: dict[str, int] = {"max": 100}
unique: set[int] = {1, 2, 3}
```

### Type Hints and Static Analysis

```python
from typing import Sequence, Callable

def process(items: Sequence[int]) -> int:
    """Sum all items in sequence."""
    return sum(items)

callback: Callable[[int, int], int] = lambda x, y: x + y
```

### First-Class Functions

```python
def apply_twice(func: Callable[[int], int], x: int) -> int:
    """Apply function twice to input."""
    return func(func(x))

result = apply_twice(lambda x: x * 2, 5)  # 20
```

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_01.py -v
```

## References

- Learning Python, 5th Edition - Part I: Getting Started
- PEP 484 - Type Hints
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
