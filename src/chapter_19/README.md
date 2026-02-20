# Chapter 19: Packaging and Distribution

## Topics Covered
- Virtual environments: `venv`, isolation, activation
- `pyproject.toml`: modern project configuration (PEP 621)
- Build backends: setuptools, hatchling, flit, Poetry
- Package structure: src-layout vs flat layout
- Entry points: console scripts and plugins
- Dependency specification and version constraints
- Building distributions: sdist and wheel
- Publishing to PyPI and private registries

## Notebooks
1. **01_virtual_environments.ipynb** — venv, isolation, pip, dependency resolution
2. **02_project_configuration.ipynb** — pyproject.toml, build backends, entry points
3. **03_building_and_publishing.ipynb** — sdist, wheels, PyPI, versioning strategies

## Key Takeaways
- Always use virtual environments for project isolation
- `pyproject.toml` is the modern standard for Python project configuration
- src-layout prevents accidental imports from the source tree
- Semantic versioning communicates change impact to users
