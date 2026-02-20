"""Tests for Chapter 11: Unicode, Text, and Bytes."""

import unicodedata


class TestStrVsBytes:
    """Test str and bytes fundamentals."""

    def test_str_is_unicode(self) -> None:
        """str objects are sequences of Unicode characters."""
        text: str = "Hello, 世界! 🌍"
        assert isinstance(text, str)
        assert len(text) == 12  # Characters, not bytes

    def test_bytes_is_raw(self) -> None:
        """bytes objects are sequences of integers 0-255."""
        data: bytes = b"Hello"
        assert isinstance(data, bytes)
        assert data[0] == 72  # ASCII value of 'H'

    def test_encode_decode_roundtrip(self) -> None:
        """str.encode() -> bytes, bytes.decode() -> str."""
        original: str = "café"
        encoded: bytes = original.encode("utf-8")
        decoded: str = encoded.decode("utf-8")
        assert decoded == original
        assert len(encoded) == 5  # 'é' is 2 bytes in UTF-8

    def test_bytearray_is_mutable(self) -> None:
        """bytearray is a mutable version of bytes."""
        data = bytearray(b"hello")
        data[0] = ord("H")
        assert data == bytearray(b"Hello")


class TestUnicode:
    """Test Unicode handling."""

    def test_unicode_normalization(self) -> None:
        """NFC and NFD are different representations of the same character."""
        # 'é' can be represented as one codepoint or two
        nfc: str = "\u00e9"  # é as single codepoint
        nfd: str = "\u0065\u0301"  # e + combining acute accent

        assert nfc != nfd  # Different byte sequences
        assert unicodedata.normalize("NFC", nfd) == nfc
        assert unicodedata.normalize("NFD", nfc) == nfd

    def test_unicode_category(self) -> None:
        """unicodedata.category returns the Unicode category."""
        assert unicodedata.category("A") == "Lu"  # Letter, uppercase
        assert unicodedata.category("3") == "Nd"  # Number, decimal digit
        assert unicodedata.category(" ") == "Zs"  # Separator, space

    def test_codepoint_name(self) -> None:
        """Unicode characters have names."""
        assert unicodedata.name("€") == "EURO SIGN"
        assert unicodedata.name("α") == "GREEK SMALL LETTER ALPHA"


class TestEncodings:
    """Test encoding patterns."""

    def test_utf8_variable_length(self) -> None:
        """UTF-8 uses 1-4 bytes per character."""
        assert len("A".encode("utf-8")) == 1
        assert len("é".encode("utf-8")) == 2
        assert len("中".encode("utf-8")) == 3
        assert len("🎉".encode("utf-8")) == 4

    def test_encoding_error_handling(self) -> None:
        """Different error handlers for encoding failures."""
        text: str = "café"
        # 'replace' substitutes unknown characters with '?'
        ascii_replaced: bytes = text.encode("ascii", errors="replace")
        assert b"?" in ascii_replaced

        # 'ignore' silently drops unknown characters
        ascii_ignored: bytes = text.encode("ascii", errors="ignore")
        assert ascii_ignored == b"caf"

    def test_latin1_is_bijective(self) -> None:
        """Latin-1 maps every byte 0-255 to a character and back."""
        for i in range(256):
            byte_val: bytes = bytes([i])
            char: str = byte_val.decode("latin-1")
            assert char.encode("latin-1") == byte_val
