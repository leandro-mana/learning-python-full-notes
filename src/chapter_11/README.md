# Chapter 11: Unicode, Text, and Bytes

Understanding Python's string model: str (Unicode text) vs bytes (raw binary), encoding/decoding, Unicode normalization, and working with binary data and protocols.

## Overview

Python 3 draws a sharp line between text (`str`, Unicode) and binary data (`bytes`/`bytearray`). This chapter covers encoding mechanics, common pitfalls, and real-world patterns for handling international text, file encodings, and binary protocols.

## Jupyter Notebooks (Primary Learning Material)

All content is delivered through interactive Jupyter notebooks. Run with:

```bash
poetry run jupyter lab src/chapter_11/
```

| Notebook | Topics |
| --- | --- |
| **01_str_vs_bytes.ipynb** | str and bytes fundamentals, encode/decode, encoding errors, bytearray |
| **02_unicode_deep_dive.ipynb** | Unicode categories, normalization (NFC/NFD/NFKC/NFKD), codepoints, grapheme clusters |
| **03_binary_and_encodings.ipynb** | Binary I/O, struct packing, base64, common encodings (UTF-8/16/32, Latin-1), BOM handling |

**Status:** Complete.

## Testing

Run tests for this chapter:
```bash
poetry run pytest tests/test_chapter_11.py -v
```

## References

- Learning Python, 5th Edition - Part II: Types and Operations (Strings)
- [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html)
- [codecs module](https://docs.python.org/3/library/codecs.html)
