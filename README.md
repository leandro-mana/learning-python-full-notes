# Learning Python - 5th Edition (Full Notes)

Study notes and examples from **"Learning Python: Powerful Object-Oriented Programming, 5th Edition"** by Mark Lutz (O'Reilly) - the definitive guide to the Python language, covering fundamental to advanced concepts through interactive Jupyter notebooks.

## Requirements

- **make** (bootstrap requirement - see below)
- Python 3.12+
- [Poetry](https://python-poetry.org/) for dependency management

## Bootstrap: Installing make

`make` is required to run the setup commands. Install it first:

```bash
# macOS (via Xcode Command Line Tools)
xcode-select --install

# Ubuntu/Debian
sudo apt-get install build-essential

# Verify installation
make --version
```

## Quick Start

```bash
# Check/install all prerequisites (Python 3.12+, Poetry)
make prereqs

# Install project dependencies
make install

# (Optional) Install pre-commit hooks for code quality on commit
make pre-commit-install

# List available chapters
make list-chapters

# List notebooks in a chapter
make list-notebooks CHAPTER=chapter_01

# Open a chapter's notebooks in Jupyter Lab
make jupyter CHAPTER=chapter_01
```

## Prerequisites

The `make prereqs` command automatically checks for:

| Prerequisite | Version |
|--------------|---------|
| Python       | 3.12+   |
| Poetry       | latest  |

## Project Structure

```bash
src/
├── common/                    # Shared utilities
│   ├── __init__.py
│   └── types.py               # Type definitions and helpers
├── chapter_01/                # Getting Started - Python Fundamentals
│   ├── README.md
│   ├── *.ipynb                # Jupyter notebooks (primary content)
│   └── data/                  # Sample data files
├── chapter_02/                # Type System and Variables
├── chapter_03/                # OOP Fundamentals
├── chapter_04/                # Advanced OOP - Classes and Inheritance
├── chapter_05/                # Decorators, Generators, and Context Managers
├── chapter_06/                # Exceptions and Error Handling
├── chapter_07/                # Modules and Packages
├── chapter_08/                # File I/O and Data Serialization
├── chapter_09/                # Iterators, Generators, and Comprehensions
├── chapter_10/                # Concurrency, Testing, and Best Practices
├── chapter_11/                # Unicode, Text, and Bytes
├── chapter_12/                # Functional Programming
├── chapter_13/                # Regular Expressions and Text Processing
├── chapter_14/                # Data Structures and Collections
├── chapter_15/                # Design Patterns and Pythonic Code
└── ...
tests/
├── conftest.py                # Shared pytest fixtures
├── test_chapter_01.py         # Chapter 1 tests
├── test_chapter_02.py
└── ...
```

## Chapters Overview

| Chapter | Topic | Key Focus | Status |
| --- | --- | --- | --- |
| 1 | Getting Started | Core syntax, data types, control flow, functions | Done |
| 2 | Type System and Variables | Type annotations, scope, namespaces, mypy | Done |
| 3 | OOP Fundamentals | Classes, methods, inheritance, encapsulation | Done |
| 4 | Advanced OOP | Multiple inheritance, MRO, metaclasses, descriptors | Done |
| 5 | Decorators, Generators, Context Managers | Decorators, yield, with statement | Done |
| 6 | Exceptions and Error Handling | Exception hierarchy, custom exceptions, EAFP, retry patterns | Done |
| 7 | Modules and Packages | Imports, packages, `__init__.py`, lazy imports, plugins | Done |
| 8 | File I/O and Data Serialization | File ops, pathlib, JSON, CSV, pickle | Done |
| 9 | Iterators and Comprehensions | Iterator protocol, advanced comprehensions, itertools | Done |
| 10 | Concurrency, Testing, Best Practices | Threading, asyncio, pytest, profiling | Done |
| 11 | Unicode, Text, and Bytes | str vs bytes, encodings, Unicode normalization | Done |
| 12 | Functional Programming | Closures, functools, operator module, composition | Done |
| 13 | Regular Expressions | re module, groups, lookahead, practical text processing | Done |
| 14 | Data Structures and Collections | Counter, defaultdict, deque, dataclasses, enums | Done |
| 15 | Design Patterns and Pythonic Code | SOLID, creational/structural/behavioral patterns | Done |

## Running Notebooks

Jupyter notebooks are the primary learning material:

```bash
# Open a specific chapter in Jupyter Lab
make jupyter CHAPTER=chapter_01

# Or launch directly with Poetry
poetry run jupyter lab src/chapter_01/
```

## Code Quality

```bash
# Run all checks (linting, formatting, types, tests)
make check

# Individual checks
make lint                 # Ruff linter
make format               # Code formatter
make type-check           # mypy type checking
make test                 # pytest
```

## Development Workflow

1. **Read the chapter** from the book
2. **Create a feature branch**: `git checkout -b feature/chapter-XX`
3. **Create notebooks** in `src/chapter_XX/`
4. **Write tests** in `tests/test_chapter_XX.py`
5. **Ensure code quality**: `make check`
6. **Create a concise README** for the chapter
7. **Commit with clear messages** and open a Pull Request

## License

This repository is for educational purposes. The book "Learning Python" is copyrighted by O'Reilly Media.
