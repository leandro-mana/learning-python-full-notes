# Learning Python - 5th Edition (Full Notes)

Study notes and examples inspired by **"Learning Python: Powerful Object-Oriented Programming, 5th Edition"** by Mark Lutz (O'Reilly) — an independent companion resource covering core Python concepts through interactive Jupyter notebooks with original code examples.

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
├── chapter_16/                # Type Hints and Static Analysis
├── chapter_17/                # Networking and Protocols
├── chapter_18/                # Database Access
├── chapter_19/                # Packaging and Distribution
├── chapter_20/                # Python Internals and Performance
├── chapter_21/                # Logging and Debugging
├── chapter_22/                # Web Development Fundamentals
├── chapter_23/                # Security and Cryptography
├── chapter_24/                # Metaprogramming
├── chapter_25/                # Python Ecosystem and Best Practices
├── chapter_26/                # Async Programming
├── chapter_27/                # Multiprocessing and Parallelism
├── chapter_28/                # Command-Line Interfaces
├── chapter_29/                # Date, Time, and Scheduling
├── chapter_30/                # XML, HTML, and Data Formats
├── chapter_31/                # String Methods and Formatting
├── chapter_32/                # Numeric Computing
├── chapter_33/                # OS and System Interaction
├── chapter_34/                # Email and Data Encoding
├── chapter_35/                # Advanced Python Patterns
├── chapter_36/                # Advanced Testing
├── chapter_37/                # Abstract Syntax Trees
├── chapter_38/                # Memory Management
├── chapter_39/                # C Interoperability
├── chapter_40/                # Import System Internals
├── chapter_41/                # Concurrency Patterns
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
| 16 | Type Hints and Static Analysis | typing module, generics, Protocol, overload, mypy | Done |
| 17 | Networking and Protocols | Sockets, HTTP, urllib, asyncio networking | Done |
| 18 | Database Access | sqlite3, DB-API, transactions, row factories | Done |
| 19 | Packaging and Distribution | venv, pyproject.toml, wheels, entry points, PyPI | Done |
| 20 | Python Internals and Performance | Memory model, GIL, profiling, bytecode, optimization | Done |
| 21 | Logging and Debugging | logging module, handlers, formatters, pdb, traceback | Done |
| 22 | Web Development Fundamentals | WSGI, HTTP servers, routing, templates, REST APIs | Done |
| 23 | Security and Cryptography | hashlib, hmac, secrets, input validation, secure coding | Done |
| 24 | Metaprogramming | Dynamic attributes, class decorators, introspection, codegen | Done |
| 25 | Python Ecosystem and Best Practices | Code style, linting, testing patterns, CI/CD, project org | Done |
| 26 | Async Programming | asyncio, async/await, tasks, gather, semaphores | Done |
| 27 | Multiprocessing and Parallelism | multiprocessing, Pool, ProcessPoolExecutor, IPC | Done |
| 28 | Command-Line Interfaces | argparse, subcommands, environment variables | Done |
| 29 | Date, Time, and Scheduling | datetime, zoneinfo, timedelta, calendar, formatting | Done |
| 30 | XML, HTML, and Data Formats | xml.etree, html.parser, configparser, struct | Done |
| 31 | String Methods and Formatting | f-strings, str methods, string module, difflib, textwrap | Done |
| 32 | Numeric Computing | math, decimal, fractions, random, statistics | Done |
| 33 | OS and System Interaction | os, shutil, tempfile, platform, subprocess | Done |
| 34 | Email and Data Encoding | email.message, base64, quopri, mimetypes, binascii | Done |
| 35 | Advanced Python Patterns | Descriptors, `__slots__`, weakrefs, ABCs, copy protocol | Done |
| 36 | Advanced Testing | pytest fixtures, parametrize, markers, unittest.mock, test patterns | Done |
| 37 | Abstract Syntax Trees | ast module, NodeVisitor, NodeTransformer, compile, eval, exec | Done |
| 38 | Memory Management | Reference counting, gc module, tracemalloc, finalize, optimization | Done |
| 39 | C Interoperability | ctypes, structures, callbacks, array module, memoryview | Done |
| 40 | Import System Internals | importlib, import hooks, sys.meta_path, pkgutil, metadata | Done |
| 41 | Concurrency Patterns | Threading sync, concurrent.futures, Queue, producer-consumer | Done |

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
