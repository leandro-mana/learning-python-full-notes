# Chapter 3: Object-Oriented Programming Fundamentals

Python's object-oriented system: classes, inheritance, methods, and encapsulation. OOP foundations for building scalable, maintainable applications.

## Overview

This chapter covers the foundations of Python's OOP model: classes as blueprints, instance vs class attributes, method types (instance, class, static), inheritance with the Method Resolution Order (MRO), and encapsulation through properties and naming conventions.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_03/
```

| Notebook | Topics |
| --- | --- |
| **01_classes_and_objects.ipynb** | Classes, `__init__`, instance attributes/methods, dunder methods (`__str__`, `__repr__`, `__add__`, `__len__`) |
| **02_methods_and_attributes.ipynb** | Instance methods, `@classmethod`, `@staticmethod`, `@property`, attribute lookup order |
| **03_inheritance_and_mro.ipynb** | Single/multiple inheritance, `super()`, Method Resolution Order (C3 linearization), polymorphism |
| **04_encapsulation_and_access_control.ipynb** | Privacy conventions (`_`, `__`), name mangling, properties for validation, `__slots__`, descriptor protocol |

## Key Concepts

### Class Definition and Methods

```python
class Person:
    """A person with name and age."""

    species: str = "Homo sapiens"  # Class attribute

    def __init__(self, name: str, age: int) -> None:
        self.name: str = name
        self.age: int = age

    def greet(self) -> str:
        """Instance method - has access to self."""
        return f"Hello, I'm {self.name}"

    @classmethod
    def from_birth_year(cls, name: str, birth_year: int) -> "Person":
        """Class method - receives class as first argument."""
        return cls(name, 2025 - birth_year)

    @staticmethod
    def is_adult(age: int) -> bool:
        """Static method - doesn't access self or class."""
        return age >= 18
```

### Inheritance and super()

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def make_sound(self) -> str:
        return "Generic animal sound"

class Dog(Animal):
    def __init__(self, name: str, breed: str) -> None:
        super().__init__(name)
        self.breed: str = breed

    def make_sound(self) -> str:
        return "Woof!"
```

### Properties for Encapsulation

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius: float = celsius

    @property
    def fahrenheit(self) -> float:
        return (self._celsius * 9 / 5) + 32

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value
```

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_03.py -v
```

## References

- Learning Python, 5th Edition - Part VI: Classes and OOP
- PEP 20 - The Zen of Python
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
