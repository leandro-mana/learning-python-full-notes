# Chapter 6: Exceptions and Error Handling

Exception hierarchy, try/except/else/finally, custom exceptions, exception chaining, and production-ready error handling patterns.

## Overview

Python's exception mechanism provides structured error management. This chapter covers the exception hierarchy, control flow through try blocks, building custom exception classes, and patterns like EAFP, retry logic, and graceful degradation.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_06/
```

| Notebook | Topics |
| --- | --- |
| **01_exception_basics.ipynb** | Exception hierarchy, try/except/else/finally, catching multiple exceptions, EAFP vs LBYL, re-raising |
| **02_custom_exceptions.ipynb** | Custom exception classes, exception chaining (`raise from`), suppressing context, ExceptionGroup |
| **03_exception_patterns.ipynb** | Retry with backoff, graceful degradation, warnings module, error boundary context managers |

## Key Concepts

### try / except / else / finally

```python
try:
    result = operation()
except SpecificError as e:
    handle_error(e)
else:
    # Only runs if no exception
    use_result(result)
finally:
    # Always runs
    cleanup()
```

### Custom Exception Hierarchy

```python
class AppError(Exception):
    """Base exception for the application."""

class ValidationError(AppError):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")
```

### Exception Chaining

```python
try:
    value = config[key]
except KeyError as e:
    raise ConfigError(f"Missing key: {key}") from e
```

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_06.py -v
```

## References

- Learning Python, 5th Edition - Part VII: Exceptions and Tools
- PEP 3134 - Exception Chaining and Embedded Tracebacks
- [Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
