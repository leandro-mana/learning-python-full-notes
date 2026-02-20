# Chapter 24: Metaprogramming

## Topics Covered
- Dynamic attribute access: `__getattr__`, `__getattribute__`, `__setattr__`
- Property factories and dynamic properties
- Class decorators: modifying classes after creation
- `__init_subclass__`: hook for subclass creation
- Import hooks: `sys.meta_path`, custom finders and loaders
- `exec()` and `eval()`: dynamic code execution (and its dangers)
- `inspect` module: introspecting live objects
- Code generation patterns

## Notebooks
1. **01_dynamic_attributes.ipynb** — `__getattr__`, `__setattr__`, property factories
2. **02_class_decorators.ipynb** — Class decorators, `__init_subclass__`, registration
3. **03_introspection_and_codegen.ipynb** — inspect module, import hooks, code generation

## Key Takeaways
- `__getattr__` enables proxy objects and lazy attributes
- Class decorators are a simpler alternative to metaclasses
- `__init_subclass__` handles most subclass registration needs
- Use metaprogramming sparingly — readability trumps cleverness
