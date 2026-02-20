"""Tests for Chapter 31: String Methods and Formatting."""

import difflib
import string
import textwrap


class TestFStringsAndFormatting:
    """Test f-string and format spec features."""

    def test_fstring_expression(self) -> None:
        """f-strings evaluate expressions inline."""
        name = "Alice"
        assert f"Hello, {name}!" == "Hello, Alice!"
        assert f"{2 + 3}" == "5"
        assert f"{'hello'.upper()}" == "HELLO"

    def test_format_spec_alignment(self) -> None:
        """Format specs control alignment and padding."""
        assert f"{'left':<10}" == "left      "
        assert f"{'right':>10}" == "     right"
        assert f"{'center':^10}" == "  center  "
        assert f"{'fill':*^10}" == "***fill***"

    def test_format_spec_numbers(self) -> None:
        """Format specs control number display."""
        assert f"{3.14159:.2f}" == "3.14"
        assert f"{1000000:,}" == "1,000,000"
        assert f"{255:08b}" == "11111111"
        assert f"{255:#x}" == "0xff"

    def test_format_spec_percentage(self) -> None:
        """Percentage format multiplies by 100."""
        assert f"{0.856:.1%}" == "85.6%"

    def test_format_method(self) -> None:
        """str.format() supports positional and keyword args."""
        assert "{} {}".format("hello", "world") == "hello world"
        assert "{name} is {age}".format(name="Alice", age=30) == "Alice is 30"


class TestStringMethods:
    """Test str methods."""

    def test_split_and_join(self) -> None:
        """split and join are inverses."""
        words = "hello world python".split()
        assert words == ["hello", "world", "python"]
        assert "-".join(words) == "hello-world-python"

    def test_strip_variants(self) -> None:
        """strip removes whitespace from edges."""
        s = "  hello  "
        assert s.strip() == "hello"
        assert s.lstrip() == "hello  "
        assert s.rstrip() == "  hello"

    def test_replace(self) -> None:
        """replace substitutes substrings."""
        assert "hello world".replace("world", "python") == "hello python"
        assert "aaa".replace("a", "b", 2) == "bba"

    def test_startswith_endswith(self) -> None:
        """startswith and endswith check prefixes/suffixes."""
        assert "hello.py".endswith(".py")
        assert "hello.py".startswith("hello")
        assert "test.txt".endswith((".txt", ".csv"))

    def test_translate_table(self) -> None:
        """maketrans and translate perform character mapping."""
        table = str.maketrans("aeiou", "12345")
        assert "hello".translate(table) == "h2ll4"

    def test_partition(self) -> None:
        """partition splits on first occurrence."""
        before, sep, after = "key=value=extra".partition("=")
        assert before == "key"
        assert sep == "="
        assert after == "value=extra"


class TestStringModule:
    """Test string module constants and templates."""

    def test_string_constants(self) -> None:
        """string module provides character sets."""
        assert "a" in string.ascii_lowercase
        assert "Z" in string.ascii_uppercase
        assert "5" in string.digits
        assert "!" in string.punctuation

    def test_string_template(self) -> None:
        """Template provides safe substitution."""
        tmpl = string.Template("Hello, $name!")
        assert tmpl.substitute(name="Alice") == "Hello, Alice!"
        assert tmpl.safe_substitute() == "Hello, $name!"


class TestDifflibAndTextwrap:
    """Test difflib and textwrap utilities."""

    def test_difflib_get_close_matches(self) -> None:
        """get_close_matches finds similar strings."""
        words = ["apple", "application", "apply", "banana"]
        matches = difflib.get_close_matches("appli", words)
        assert "application" in matches or "apply" in matches

    def test_difflib_sequence_matcher(self) -> None:
        """SequenceMatcher computes similarity ratio."""
        ratio = difflib.SequenceMatcher(None, "hello", "hallo").ratio()
        assert 0.7 < ratio < 1.0

    def test_textwrap_wrap(self) -> None:
        """textwrap.wrap breaks text into lines."""
        text = "This is a long sentence that should be wrapped at a certain width."
        lines = textwrap.wrap(text, width=30)
        assert all(len(line) <= 30 for line in lines)

    def test_textwrap_shorten(self) -> None:
        """textwrap.shorten truncates with placeholder."""
        text = "Hello World, this is a long string"
        short = textwrap.shorten(text, width=20)
        assert len(short) <= 20
        assert short.endswith("[...]")
