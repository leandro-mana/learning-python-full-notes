"""Tests for Chapter 13: Regular Expressions and Text Processing."""

import re


class TestRegexFundamentals:
    """Test basic regex operations."""

    def test_match_vs_search(self) -> None:
        """match checks start of string; search scans the whole string."""
        text: str = "Hello, World!"

        assert re.match(r"Hello", text) is not None
        assert re.match(r"World", text) is None  # Not at start
        assert re.search(r"World", text) is not None  # Found anywhere

    def test_findall_returns_all_matches(self) -> None:
        """findall returns a list of all non-overlapping matches."""
        text: str = "The year 2024 and 2025 are important"
        years: list[str] = re.findall(r"\d{4}", text)
        assert years == ["2024", "2025"]

    def test_character_classes(self) -> None:
        """Character classes match sets of characters."""
        assert re.findall(r"[aeiou]", "hello world") == ["e", "o", "o"]
        assert re.findall(r"\d+", "abc123def456") == ["123", "456"]

    def test_quantifiers(self) -> None:
        """Quantifiers control repetition."""
        assert re.findall(r"ab?c", "ac abc abbc") == ["ac", "abc"]
        assert re.findall(r"ab+c", "ac abc abbc") == ["abc", "abbc"]
        assert re.findall(r"ab*c", "ac abc abbc") == ["ac", "abc", "abbc"]


class TestGroupsAndAdvanced:
    """Test groups and advanced regex features."""

    def test_capturing_groups(self) -> None:
        """Parentheses create capturing groups."""
        match = re.search(r"(\d{4})-(\d{2})-(\d{2})", "Date: 2024-01-15")
        assert match is not None
        assert match.group(1) == "2024"
        assert match.group(2) == "01"
        assert match.group(3) == "15"

    def test_named_groups(self) -> None:
        """Named groups are accessed by name."""
        pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
        match = re.search(pattern, "Date: 2024-01-15")
        assert match is not None
        assert match.group("year") == "2024"
        assert match.group("month") == "01"

    def test_lookahead(self) -> None:
        """Lookahead asserts what follows without consuming."""
        # Find words followed by a comma
        result = re.findall(r"\w+(?=,)", "hello, world, python")
        assert result == ["hello", "world"]

    def test_substitution(self) -> None:
        """re.sub replaces matches."""
        result = re.sub(r"\d+", "NUM", "I have 3 cats and 5 dogs")
        assert result == "I have NUM cats and NUM dogs"


class TestPracticalPatterns:
    """Test practical regex patterns."""

    def test_email_validation(self) -> None:
        """Simple email pattern matching."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        assert re.match(pattern, "user@example.com") is not None
        assert re.match(pattern, "not-an-email") is None

    def test_split_with_regex(self) -> None:
        """re.split for complex splitting."""
        # Split on any whitespace or comma
        result = re.split(r"[,\s]+", "one, two  three,four")
        assert result == ["one", "two", "three", "four"]

    def test_compiled_pattern(self) -> None:
        """Compiled patterns are reusable and efficient."""
        pattern = re.compile(r"\b\w{5}\b")
        assert pattern.findall("I love happy short words today") == [
            "happy",
            "short",
            "words",
            "today",
        ]
