"""Tests for Chapter 34: Email and Data Encoding."""

import base64
import binascii
import mimetypes
import quopri
from email.message import EmailMessage


class TestEmailMessages:
    """Test email message construction."""

    def test_email_basic(self) -> None:
        """EmailMessage creates a basic email."""
        msg = EmailMessage()
        msg["Subject"] = "Test"
        msg["From"] = "alice@example.com"
        msg["To"] = "bob@example.com"
        msg.set_content("Hello, Bob!")

        assert msg["Subject"] == "Test"
        assert msg["From"] == "alice@example.com"
        assert "Hello, Bob!" in msg.get_content()

    def test_email_headers(self) -> None:
        """Email headers are case-insensitive."""
        msg = EmailMessage()
        msg["Content-Type"] = "text/plain"
        assert msg["content-type"] == "text/plain"

    def test_email_multipart(self) -> None:
        """EmailMessage supports multipart messages."""
        msg = EmailMessage()
        msg["Subject"] = "With attachment"
        msg.set_content("Main body")
        msg.add_attachment(
            b"file content",
            maintype="application",
            subtype="octet-stream",
            filename="data.bin",
        )
        assert msg.is_multipart()

    def test_email_as_string(self) -> None:
        """EmailMessage serializes to string."""
        msg = EmailMessage()
        msg["Subject"] = "Hello"
        msg.set_content("Body text")
        text = msg.as_string()
        assert "Subject: Hello" in text
        assert "Body text" in text


class TestMimeTypes:
    """Test MIME type detection."""

    def test_guess_type(self) -> None:
        """mimetypes.guess_type identifies file types."""
        mime, _ = mimetypes.guess_type("document.pdf")
        assert mime == "application/pdf"

        mime, _ = mimetypes.guess_type("image.png")
        assert mime == "image/png"

        mime, _ = mimetypes.guess_type("script.py")
        assert mime == "text/x-python"

    def test_guess_extension(self) -> None:
        """mimetypes.guess_extension finds extensions."""
        ext = mimetypes.guess_extension("text/html")
        assert ext in (".html", ".htm")

    def test_common_types(self) -> None:
        """Common MIME types are well-known."""
        assert mimetypes.guess_type("file.json")[0] == "application/json"
        assert mimetypes.guess_type("file.csv")[0] == "text/csv"
        assert mimetypes.guess_type("file.txt")[0] == "text/plain"


class TestBase64Encoding:
    """Test base64 encoding/decoding."""

    def test_base64_encode_decode(self) -> None:
        """base64 encodes bytes to ASCII and back."""
        original = b"Hello, World!"
        encoded = base64.b64encode(original)
        assert isinstance(encoded, bytes)
        decoded = base64.b64decode(encoded)
        assert decoded == original

    def test_base64_urlsafe(self) -> None:
        """URL-safe base64 uses - and _ instead of + and /."""
        data = bytes(range(256))
        encoded = base64.urlsafe_b64encode(data)
        assert b"+" not in encoded
        assert b"/" not in encoded
        assert base64.urlsafe_b64decode(encoded) == data

    def test_base64_string(self) -> None:
        """base64 works with string data via encode/decode."""
        text = "Python is great!"
        encoded = base64.b64encode(text.encode()).decode()
        assert isinstance(encoded, str)
        decoded = base64.b64decode(encoded).decode()
        assert decoded == text


class TestQuopriAndBinascii:
    """Test quoted-printable and binary-ASCII conversions."""

    def test_quopri_encode(self) -> None:
        """quopri encodes non-ASCII as =XX sequences."""
        data = "Héllo Wörld".encode("utf-8")
        encoded = quopri.encodestring(data)
        assert b"=C3" in encoded  # UTF-8 for accented chars

    def test_quopri_decode(self) -> None:
        """quopri decodes =XX sequences back to bytes."""
        encoded = b"Hello=20World"
        decoded = quopri.decodestring(encoded)
        assert decoded == b"Hello World"

    def test_binascii_hexlify(self) -> None:
        """binascii converts between binary and hex."""
        data = b"\xde\xad\xbe\xef"
        hex_str = binascii.hexlify(data)
        assert hex_str == b"deadbeef"
        assert binascii.unhexlify(hex_str) == data

    def test_binascii_crc32(self) -> None:
        """binascii.crc32 computes CRC-32 checksums."""
        crc = binascii.crc32(b"hello")
        assert isinstance(crc, int)
        assert crc == binascii.crc32(b"hello")  # deterministic
