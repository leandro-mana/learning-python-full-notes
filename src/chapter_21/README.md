# Chapter 21: Logging and Debugging

## Topics Covered
- `logging` module: loggers, handlers, formatters, filters
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Handler types: StreamHandler, FileHandler, RotatingFileHandler
- Formatter patterns and structured logging
- Logger hierarchy and propagation
- `pdb` debugger: breakpoints, stepping, inspecting
- `breakpoint()` built-in (Python 3.7+)
- Debugging strategies and common patterns

## Notebooks
1. **01_logging_fundamentals.ipynb** — Loggers, handlers, formatters, log levels
2. **02_advanced_logging.ipynb** — Hierarchy, filters, rotating files, structured logging
3. **03_debugging_techniques.ipynb** — pdb, breakpoint(), debugging strategies, traceback

## Key Takeaways
- Use logging instead of print() for production code
- Configure logging once at application startup
- Logger hierarchy enables fine-grained control per module
- pdb and breakpoint() are essential debugging tools
