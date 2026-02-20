"""Tests for Chapter 23: Security and Cryptography."""

import hashlib
import hmac
import secrets


class TestHashing:
    """Test hashlib and hashing patterns."""

    def test_sha256_digest(self) -> None:
        """SHA-256 produces a 64-character hex digest."""
        digest = hashlib.sha256(b"hello world").hexdigest()
        assert len(digest) == 64
        # Same input always produces same hash
        assert digest == hashlib.sha256(b"hello world").hexdigest()

    def test_different_inputs_different_hashes(self) -> None:
        """Different inputs produce different hashes."""
        h1 = hashlib.sha256(b"hello").hexdigest()
        h2 = hashlib.sha256(b"world").hexdigest()
        assert h1 != h2

    def test_blake2b_digest(self) -> None:
        """BLAKE2b is a fast, secure hash function."""
        h = hashlib.blake2b(b"hello", digest_size=32)
        assert len(h.hexdigest()) == 64

    def test_incremental_hashing(self) -> None:
        """update() allows incremental hashing of large data."""
        h1 = hashlib.sha256(b"helloworld").hexdigest()

        h2 = hashlib.sha256()
        h2.update(b"hello")
        h2.update(b"world")

        assert h1 == h2.hexdigest()


class TestHMAC:
    """Test HMAC message authentication."""

    def test_hmac_creation(self) -> None:
        """HMAC combines a key with a message hash."""
        key = b"secret-key"
        message = b"important data"
        mac = hmac.new(key, message, hashlib.sha256)
        assert len(mac.hexdigest()) == 64

    def test_hmac_verification(self) -> None:
        """HMAC verification uses constant-time comparison."""
        key = b"secret-key"
        message = b"important data"
        mac1 = hmac.new(key, message, hashlib.sha256).hexdigest()
        mac2 = hmac.new(key, message, hashlib.sha256).hexdigest()
        assert hmac.compare_digest(mac1, mac2)

    def test_hmac_different_keys(self) -> None:
        """Different keys produce different MACs."""
        message = b"same message"
        mac1 = hmac.new(b"key1", message, hashlib.sha256).hexdigest()
        mac2 = hmac.new(b"key2", message, hashlib.sha256).hexdigest()
        assert mac1 != mac2


class TestSecrets:
    """Test secrets module for secure random values."""

    def test_token_hex(self) -> None:
        """token_hex generates a random hex string."""
        token = secrets.token_hex(32)
        assert len(token) == 64  # 32 bytes = 64 hex chars
        assert isinstance(token, str)

    def test_token_bytes(self) -> None:
        """token_bytes generates random bytes."""
        token = secrets.token_bytes(16)
        assert len(token) == 16
        assert isinstance(token, bytes)

    def test_token_urlsafe(self) -> None:
        """token_urlsafe generates URL-safe base64 tokens."""
        token = secrets.token_urlsafe(32)
        assert isinstance(token, str)
        # URL-safe characters only
        safe_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")
        assert all(c in safe_chars for c in token)

    def test_compare_digest_constant_time(self) -> None:
        """compare_digest prevents timing attacks."""
        a = "correct_token"
        b = "correct_token"
        assert secrets.compare_digest(a, b)
        assert not secrets.compare_digest(a, "wrong_token")
