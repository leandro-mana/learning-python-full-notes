# Chapter 15: Design Patterns and Pythonic Code

Classic design patterns adapted for Python, SOLID principles, and idiomatic Python conventions that separate good code from great code.

## Overview

Design patterns in Python look different from Java or C++ because Python's dynamic nature and first-class functions simplify many traditional patterns. This chapter covers the most useful patterns (Strategy, Observer, Factory, Decorator, Singleton), SOLID principles in Python, and idiomatic coding conventions.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_15/
```

| Notebook | Topics |
| --- | --- |
| **01_solid_principles.ipynb** | Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion |
| **02_creational_and_structural.ipynb** | Factory, Builder, Singleton (Pythonic), Adapter, Facade, Proxy |
| **03_behavioral_patterns.ipynb** | Strategy, Observer, Command, Template Method, Iterator, State |

**Status:** Complete.

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_15.py -v
```

## References

- Learning Python, 5th Edition - Part VI: Classes and OOP
- [Design Patterns in Python](https://refactoring.guru/design-patterns/python)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
