# Contributing to Learning Python

This repository follows a professional, chapter-based workflow inspired by the [data-algorithms-with-pyspark](https://github.com/leandromana/data-algorithms-with-pyspark) repository pattern.

## Workflow

### 1. Branch per Chapter

Create a feature branch for each chapter:

```bash
git checkout -b feature/chapter-01
git checkout -b feature/chapter-02
```

### 2. Chapter Structure

Each chapter directory should contain:

```bash
src/chapter_XX/
├── __init__.py            # Module docstring describing the chapter
├── README.md              # Chapter overview, notebook table, key concepts
├── 01_topic_name.ipynb    # Jupyter notebooks (primary content)
├── 02_another_topic.ipynb
└── data/                  # Sample data files if needed
```

### 3. Jupyter Notebooks

Notebooks are the primary learning material. When creating them:

1. Keep each notebook focused on one topic
2. Interleave markdown explanations with executable code cells
3. Number notebooks sequentially: `01_topic_name.ipynb`, `02_another_topic.ipynb`
4. Include output for key demonstrations
5. Reference the book chapter and section numbers
6. Use type hints in code cells

```bash
# Open notebooks for editing
make jupyter CHAPTER=chapter_XX
```

### 4. Chapter READMEs

Each chapter README should include:

- **Overview**: Brief chapter summary
- **Notebooks table**: All notebooks with topics covered
- **Key Concepts**: Code examples showing main ideas
- **Testing**: How to run chapter tests
- **References**: Links to book sections and external resources

### 5. Write Tests

Add tests for each chapter in `tests/test_chapter_XX.py`:

```python
"""Tests for Chapter XX: Topic Name."""

import pytest


class TestConceptName:
    """Test concept from Chapter XX."""

    def test_specific_behavior(self) -> None:
        """Description of what's being tested."""
        result = some_operation()
        assert result == expected_value
```

Tests should verify the concepts covered in notebooks - they serve as executable documentation.

### 6. Code Quality

Before committing, run all checks:

```bash
# Single command to check everything
make check

# Or individual checks
make lint              # Ruff linter
make format            # Code formatting
make type-check        # mypy type checking
make test              # pytest
```

### 7. Commit Messages

Write clear commit messages:

- `feat(ch01): Add core concepts and control flow notebooks`
- `test(ch02): Add type system and scoping tests`
- `docs(ch03): Update OOP chapter README`
- `fix(ch04): Fix metaclass example in notebook`
- `refactor(ch05): Reorganize decorator examples`

### 8. Pull Request

When ready, open a PR with:

- Clear title: `Add Chapter 3 - OOP Fundamentals`
- Description of notebooks included and concepts covered

## Code Style

Enforced by `make format` (ruff):

- Line length: 100 characters
- 4 spaces for indentation
- f-strings for formatting
- snake_case for functions/variables
- PascalCase for classes
- UPPER_CASE for constants

## Testing Requirements

- All chapters should have corresponding test files
- Tests verify the concepts, not just run without error
- Use pytest fixtures for common setup (see `conftest.py`)
- Class-based test organization matching chapter topics
