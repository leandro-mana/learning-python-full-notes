# Chapter 2: Type System and Variables

Deep exploration of Python's type system, type annotations, variable scope, namespaces, and how Python resolves names at runtime.

## Overview

Understanding Python's type system and scoping rules is essential for writing maintainable, self-documenting code at scale. This chapter covers variable binding and references, scope and namespaces, type annotations and the typing module, and static analysis with mypy.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_02/
```

| Notebook | Topics |
| --- | --- |
| **01_variables_and_binding.ipynb** | Object references, aliasing, shallow vs deep copy, immutable vs mutable rebinding |
| **02_scope_and_namespaces.ipynb** | LEGB rule, global/nonlocal keywords, closures, namespace introspection |
| **03_static_analysis_mypy.ipynb** | mypy configuration, type checking strategies, cast() usage, type narrowing |
| **04_type_annotations_deep_dive.ipynb** | PEP 484 fundamentals, generics with TypeVar, Protocol for structural subtyping |

## Key Concepts

### Scope and Namespaces (LEGB Rule)

```python
global_var: str = "global"

def outer() -> None:
    enclosing_var: str = "enclosing"

    def inner() -> None:
        local_var: str = "local"
        print(local_var)  # Finds local_var first (LEGB rule)

    inner()
```

### Closures and Variable Capture

```python
from typing import Callable

def make_multiplier(factor: int) -> Callable[[int], int]:
    """Create a multiplier function with captured factor."""

    def multiply(x: int) -> int:
        return x * factor  # Captures factor from enclosing scope

    return multiply

times_three = make_multiplier(3)
print(times_three(5))  # 15
```

### Generic Types and TypeVar

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    """Type-safe stack implementation."""

    def __init__(self) -> None:
        self.items: list[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()
```

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_02.py -v
```

## References

- Learning Python, 5th Edition - Part II: Types and Operations
- PEP 484 - Type Hints
- PEP 585 - Type Hinting Generics in Standard Collections
- [mypy Documentation](https://mypy.readthedocs.io/)
