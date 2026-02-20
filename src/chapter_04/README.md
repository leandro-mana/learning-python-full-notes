# Chapter 4: Advanced OOP - Classes and Inheritance

Advanced object-oriented design: multiple inheritance, Method Resolution Order (MRO), metaclasses, abstract base classes, descriptors, and design patterns for complex hierarchies.

## Overview

This chapter tackles the more sophisticated aspects of Python's OOP model. Understanding MRO is critical for working with multiple inheritance. Metaclasses and descriptors enable powerful abstractions that separate junior from senior developers.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_04/
```

| Notebook | Topics |
| --- | --- |
| **01_mro_and_multiple_inheritance.ipynb** | Multiple inheritance, C3 linearization, MRO, diamond problem, `super()` chain |
| **02_metaclasses.ipynb** | `type()`, `__new__` vs `__init__`, metaclass patterns (singleton, registry, validation) |
| **03_descriptors_and_abcs.ipynb** | Descriptor protocol (`__get__`, `__set__`, `__delete__`), ABC, `@abstractmethod`, mixins |

**Status:** Complete.

## Key Concepts

### Multiple Inheritance and MRO

```python
class A:
    def method(self) -> str:
        return "A"

class B(A):
    def method(self) -> str:
        return "B"

class C(A):
    def method(self) -> str:
        return "C"

class D(B, C):
    pass

print(D.mro())  # [D, B, C, A, object]
d = D()
print(d.method())  # "B" - follows MRO
```

### Metaclasses

```python
class SingletonMeta(type):
    """Metaclass that enforces singleton pattern."""

    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.connection = None

db1 = Database()
db2 = Database()
assert db1 is db2  # True - same object
```

### Descriptors

```python
class ValidatedString:
    """Descriptor that validates string assignments."""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, obj: object, objtype: type | None = None) -> str | None:
        if obj is None:
            return self
        return obj.__dict__.get(self.name, None)

    def __set__(self, obj: object, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be str")
        if len(value) == 0:
            raise ValueError(f"{self.name} cannot be empty")
        obj.__dict__[self.name] = value
```

### Mixin Pattern

```python
class Serializable:
    def to_dict(self) -> dict:
        return self.__dict__.copy()

class Loggable:
    def log(self, message: str) -> None:
        print(f"[{self.__class__.__name__}] {message}")

class User(Serializable, Loggable):
    def __init__(self, name: str) -> None:
        self.name = name
```

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_04.py -v
```

## References

- Learning Python, 5th Edition - Part VI: Classes and OOP (Advanced Topics)
- PEP 3119 - Abstract Base Classes
- [Descriptor Protocol](https://docs.python.org/3/howto/descriptor.html)
- [Method Resolution Order](https://docs.python.org/3/library/stdtypes.html#class.__mro__)
