# Chapter 38: Memory Management

## Topics Covered

- Reference counting with sys.getrefcount
- gc module: collect, get_referrers, callbacks, circular references
- `__del__` finalizer and weakref.finalize
- tracemalloc for memory profiling
- Memory optimization techniques

## Notebooks

1. **01_reference_counting.ipynb** - sys.getrefcount, reference cycles, gc module
2. **02_garbage_collection.ipynb** - gc.collect, circular references, `__del__`, finalize
3. **03_memory_profiling.ipynb** - tracemalloc, sys.getsizeof, memory optimization
