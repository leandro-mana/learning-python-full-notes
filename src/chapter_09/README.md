# Chapter 9: Iterators, Generators, and Comprehensions

Iterator protocol, advanced comprehensions, built-in iteration tools, itertools module, and lazy evaluation patterns.

## Overview

Iteration is central to Python. This chapter goes deep on the iterator protocol, advanced comprehension patterns, and the itertools module for building efficient, memory-friendly data pipelines.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_09/
```

| Notebook | Topics |
| --- | --- |
| **01_iteration_protocol.ipynb** | Iterable vs Iterator, `__iter__`/`__next__`, custom iterators, StopIteration, iter() sentinel form |
| **02_advanced_comprehensions.ipynb** | Nested comprehensions, dict/set comprehensions, generator expressions, walrus operator (:=) |
| **03_itertools_recipes.ipynb** | chain, islice, groupby, product, combinations, accumulate, lazy data pipelines |

## Key Concepts

### Iterator Protocol

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1
```

### Generator Expressions vs List Comprehensions

```python
# List comprehension - builds entire list in memory
squares_list = [x**2 for x in range(1_000_000)]

# Generator expression - lazy, memory efficient
squares_gen = (x**2 for x in range(1_000_000))
```

### itertools Pipelines

```python
from itertools import chain, islice, groupby

# Chain multiple iterables
combined = chain(range(3), range(10, 13))

# Lazy slicing
first_five = islice(range(1000), 5)
```

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_09.py -v
```

## References

- Learning Python, 5th Edition - Part IV: Functions and Generators
- PEP 572 - Assignment Expressions (Walrus Operator)
- [itertools documentation](https://docs.python.org/3/library/itertools.html)
- [Iterator Types](https://docs.python.org/3/library/stdtypes.html#iterator-types)
