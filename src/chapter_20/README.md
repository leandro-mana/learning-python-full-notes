# Chapter 20: Python Internals and Performance

## Topics Covered
- CPython internals: reference counting, garbage collection
- The GIL (Global Interpreter Lock): what it is, when it matters
- Memory model: `id()`, `is` vs `==`, interning, `sys.getsizeof()`
- `__slots__` for memory optimization
- Profiling: `cProfile`, `timeit`, `line_profiler` concepts
- Optimization techniques: algorithmic improvements, caching, lazy evaluation
- `dis` module: bytecode disassembly
- C extensions overview: `ctypes`, `cffi`, Cython concepts

## Notebooks
1. **01_memory_and_gc.ipynb** — Reference counting, garbage collection, memory inspection
2. **02_profiling_and_timeit.ipynb** — cProfile, timeit, identifying bottlenecks
3. **03_optimization_techniques.ipynb** — Algorithmic improvements, bytecode, C extensions

## Key Takeaways
- Profile before optimizing — measure, don't guess
- The GIL affects CPU-bound threads but not I/O-bound or multiprocessing
- `__slots__` and generators reduce memory usage significantly
- Algorithmic improvements beat micro-optimizations every time
