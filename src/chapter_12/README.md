# Chapter 12: Functional Programming

Functional programming in Python: closures, higher-order functions, functools utilities, the operator module, and functional composition patterns.

## Overview

Python is not a purely functional language, but it has excellent support for functional programming patterns. This chapter covers closures, `functools` utilities like `partial`, `lru_cache`, and `singledispatch`, the `operator` module, and how to compose functions into data pipelines.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_12/
```

| Notebook | Topics |
| --- | --- |
| **01_closures_and_higher_order.ipynb** | Closures, higher-order functions, map/filter/reduce, lambda best practices |
| **02_functools.ipynb** | partial, lru_cache, cache, singledispatch, total_ordering, wraps, reduce |
| **03_functional_patterns.ipynb** | operator module, function composition, pipelines, immutability patterns |

**Status:** Complete.

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_12.py -v
```

## References

- Learning Python, 5th Edition - Part IV: Functions and Generators
- [functools module](https://docs.python.org/3/library/functools.html)
- [operator module](https://docs.python.org/3/library/operator.html)
