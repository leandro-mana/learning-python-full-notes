# Chapter 13: Regular Expressions and Text Processing

Mastering Python's `re` module: pattern syntax, groups, lookahead/lookbehind, and practical text parsing and transformation recipes.

## Overview

Regular expressions are a powerful tool for pattern matching, validation, and text transformation. This chapter covers the `re` module from basic patterns through advanced features like lookahead/lookbehind, named groups, and compiled patterns, with practical real-world examples.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_13/
```

| Notebook | Topics |
| --- | --- |
| **01_regex_fundamentals.ipynb** | Pattern syntax, character classes, quantifiers, anchors, match vs search vs findall |
| **02_groups_and_advanced.ipynb** | Capturing groups, named groups, backreferences, lookahead/lookbehind, flags |
| **03_practical_text_processing.ipynb** | Log parsing, data extraction, validation patterns, substitution, template engines |

**Status:** Complete.

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_13.py -v
```

## References

- Learning Python, 5th Edition - Part II: Types and Operations (String Methods)
- [re module](https://docs.python.org/3/library/re.html)
- [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html)
