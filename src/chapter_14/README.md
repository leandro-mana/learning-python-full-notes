# Chapter 14: Data Structures and Collections

Python's built-in and standard library data structures: the collections module, dataclasses, enums, and choosing the right data structure for the job.

## Overview

Beyond lists and dicts, Python provides specialized data structures for common patterns. This chapter covers `collections` (Counter, defaultdict, deque, OrderedDict, ChainMap), `dataclasses` for structured data, `enum` for type-safe constants, and guidance on choosing the right structure.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_14/
```

| Notebook | Topics |
| --- | --- |
| **01_collections_module.ipynb** | Counter, defaultdict, deque, OrderedDict, ChainMap, namedtuple |
| **02_dataclasses_and_namedtuple.ipynb** | @dataclass, field(), frozen, slots, post_init, NamedTuple, comparison |
| **03_enums_and_choosing_structures.ipynb** | Enum, IntEnum, Flag, auto(), StrEnum, choosing the right data structure |

**Status:** Complete.

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_14.py -v
```

## References

- Learning Python, 5th Edition - Part II: Types and Operations
- [collections module](https://docs.python.org/3/library/collections.html)
- [dataclasses module](https://docs.python.org/3/library/dataclasses.html)
- [enum module](https://docs.python.org/3/library/enum.html)
