# Chapter 7: Modules and Packages

Module structure, import mechanisms, package organization, namespace packages, and project layout best practices.

## Overview

Modules and packages are Python's primary code organization tools. This chapter covers how modules work under the hood, the import system, package structure with `__init__.py`, and advanced patterns like lazy imports and plugin systems.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_07/
```

| Notebook | Topics |
| --- | --- |
| **01_module_basics.ipynb** | import variants, sys.path, `__name__`/`__main__`, module attributes, dir(), reload |
| **02_packages_and_imports.ipynb** | Package structure, `__init__.py`, absolute vs relative imports, `__all__`, circular imports |
| **03_module_patterns.ipynb** | Lazy imports, plugin/registry pattern, conditional imports, module `__getattr__` (PEP 562) |

## Key Concepts

### The __name__ Guard

```python
def main() -> None:
    print("Running as script")

if __name__ == "__main__":
    main()
```

### Package Structure

```bash
mypackage/
├── __init__.py      # Package initialization
├── core.py          # Core module
├── utils.py         # Utilities
└── subpackage/
    ├── __init__.py
    └── helpers.py
```

### Import Patterns

```python
import json                          # Full module
from pathlib import Path             # Specific name
from collections import defaultdict  # Specific class
import numpy as np                   # Alias
```

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_07.py -v
```

## References

- Learning Python, 5th Edition - Part V: Modules and Packages
- PEP 328 - Imports: Multi-Line and Absolute/Relative
- PEP 562 - Module __getattr__ and __dir__
- [The Import System](https://docs.python.org/3/reference/import.html)
