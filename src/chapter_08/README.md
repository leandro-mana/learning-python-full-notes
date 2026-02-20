# Chapter 8: File I/O and Data Serialization

File operations, text vs binary modes, pathlib, JSON/CSV/pickle serialization, and data pipeline patterns.

## Overview

File I/O is fundamental to real-world Python. This chapter covers core file operations, modern path handling with pathlib, and serialization formats (JSON, CSV, pickle) for data persistence and interchange.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_08/
```

| Notebook | Topics |
| --- | --- |
| **01_file_operations.ipynb** | open() modes, reading/writing, context managers, text vs binary, encoding, seek/tell |
| **02_pathlib_and_os.ipynb** | Path construction, directory ops, glob/rglob, file metadata, tempfile, shutil |
| **03_data_serialization.ipynb** | JSON (custom encoders), CSV (DictReader/Writer), pickle (security), struct, config loader |

## Key Concepts

### Safe File I/O with Context Managers

```python
from pathlib import Path

path = Path("data.txt")
path.write_text("Hello, World!", encoding="utf-8")
content = path.read_text(encoding="utf-8")
```

### JSON Serialization

```python
import json

data = {"name": "Alice", "scores": [95, 87, 92]}
json_str = json.dumps(data, indent=2)
parsed = json.loads(json_str)
```

### pathlib for Modern Path Handling

```python
from pathlib import Path

project = Path("/Users/dev/project")
config = project / "config" / "settings.json"
for py_file in project.rglob("*.py"):
    print(py_file.name)
```

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_08.py -v
```

## References

- Learning Python, 5th Edition - Part V: Modules and Packages (File Tools)
- [pathlib documentation](https://docs.python.org/3/library/pathlib.html)
- [json module](https://docs.python.org/3/library/json.html)
- [csv module](https://docs.python.org/3/library/csv.html)
