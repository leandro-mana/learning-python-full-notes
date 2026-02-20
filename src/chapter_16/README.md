# Chapter 16: Type Hints and Static Analysis

## Topics Covered
- Type annotation syntax and evolution (PEP 484, 526, 604)
- Built-in generics: `list[int]`, `dict[str, Any]`, `tuple[int, ...]`
- `typing` module: `TypeVar`, `Generic`, `ParamSpec`, `TypeAlias`
- Union types, Optional, and the `X | Y` syntax (3.10+)
- `Protocol` for structural subtyping
- `@overload` for multiple signatures
- `TypedDict`, `Literal`, `Final`, `ClassVar`
- `mypy` configuration and common patterns
- Runtime type checking vs static analysis

## Notebooks
1. **01_annotation_fundamentals.ipynb** — Variables, functions, classes, generics
2. **02_advanced_typing.ipynb** — TypeVar, Protocol, overload, TypedDict, Literal
3. **03_mypy_in_practice.ipynb** — Configuration, common errors, gradual typing strategies

## Key Takeaways
- Type hints are documentation that tools can verify
- Use generics for reusable, type-safe containers and functions
- Protocol enables duck typing with static verification
- Gradual typing lets you add hints incrementally to existing code
