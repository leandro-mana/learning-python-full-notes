"""Tests for Chapter 30: XML, HTML, and Data Formats."""

import configparser
import csv
import io
import struct
import xml.etree.ElementTree as ET
from html import escape, unescape
from html.parser import HTMLParser


class TestXMLProcessing:
    """Test XML parsing and generation."""

    def test_parse_xml_string(self) -> None:
        """ElementTree parses XML from strings."""
        xml = "<root><item>hello</item><item>world</item></root>"
        root = ET.fromstring(xml)
        assert root.tag == "root"
        items = root.findall("item")
        assert len(items) == 2
        assert items[0].text == "hello"

    def test_build_xml(self) -> None:
        """Elements can be built programmatically."""
        root = ET.Element("catalog")
        book = ET.SubElement(root, "book", attrib={"id": "1"})
        title = ET.SubElement(book, "title")
        title.text = "Python"

        assert root.find("book") is not None
        assert root.find("book/title").text == "Python"
        assert root.find("book").get("id") == "1"

    def test_xpath_search(self) -> None:
        """XPath expressions search the XML tree."""
        xml = """<store>
            <book category="fiction"><title>Novel</title></book>
            <book category="tech"><title>Python</title></book>
        </store>"""
        root = ET.fromstring(xml)
        titles = [el.text for el in root.findall(".//title")]
        assert titles == ["Novel", "Python"]

    def test_xml_to_string(self) -> None:
        """tostring converts elements back to XML."""
        root = ET.Element("msg")
        root.text = "hello"
        result = ET.tostring(root, encoding="unicode")
        assert "<msg>hello</msg>" in result


class TestHTMLProcessing:
    """Test HTML parsing and escaping."""

    def test_html_escape(self) -> None:
        """html.escape prevents XSS."""
        dangerous = '<script>alert("xss")</script>'
        safe = escape(dangerous)
        assert "<script>" not in safe
        assert "&lt;script&gt;" in safe

    def test_html_unescape(self) -> None:
        """html.unescape reverses escaping."""
        escaped = "&lt;b&gt;bold&lt;/b&gt;"
        assert unescape(escaped) == "<b>bold</b>"

    def test_html_parser_extracts_tags(self) -> None:
        """HTMLParser can extract tags from HTML."""
        tags: list[str] = []

        class TagCollector(HTMLParser):
            def handle_starttag(self, tag: str, attrs: list) -> None:
                tags.append(tag)

        parser = TagCollector()
        parser.feed("<html><body><p>Hello</p><a href='#'>Link</a></body></html>")
        assert "html" in tags
        assert "p" in tags
        assert "a" in tags

    def test_html_parser_extracts_data(self) -> None:
        """HTMLParser can extract text content."""
        texts: list[str] = []

        class TextCollector(HTMLParser):
            def handle_data(self, data: str) -> None:
                stripped = data.strip()
                if stripped:
                    texts.append(stripped)

        parser = TextCollector()
        parser.feed("<p>Hello</p><p>World</p>")
        assert texts == ["Hello", "World"]


class TestConfigFormats:
    """Test configuration file formats."""

    def test_configparser_read(self) -> None:
        """configparser reads INI-style config files."""
        config_str = """
[database]
host = localhost
port = 5432
name = mydb

[debug]
enabled = true
"""
        config = configparser.ConfigParser()
        config.read_string(config_str)

        assert config["database"]["host"] == "localhost"
        assert config.getint("database", "port") == 5432
        assert config.getboolean("debug", "enabled") is True

    def test_configparser_defaults(self) -> None:
        """configparser supports default values."""
        config = configparser.ConfigParser()
        config.read_string("[section]\nkey = value")
        assert config.get("section", "key") == "value"
        assert config.get("section", "missing", fallback="default") == "default"

    def test_configparser_write(self) -> None:
        """configparser can write config files."""
        config = configparser.ConfigParser()
        config["app"] = {"name": "myapp", "version": "1.0"}
        output = io.StringIO()
        config.write(output)
        written = output.getvalue()
        assert "myapp" in written
        assert "1.0" in written


class TestAdvancedDataFormats:
    """Test CSV dialects and struct packing."""

    def test_csv_dialect(self) -> None:
        """CSV dialects customize parsing behavior."""
        data = "name|age|city\nAlice|30|NYC\nBob|25|LA"
        reader = csv.DictReader(io.StringIO(data), delimiter="|")
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["name"] == "Alice"
        assert rows[1]["city"] == "LA"

    def test_csv_quoting(self) -> None:
        """CSV handles quoted fields with special characters."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["name", "note"])
        writer.writerow(["Alice", 'She said "hello"'])
        content = output.getvalue()
        assert '"She said ""hello"""' in content

    def test_struct_pack_unpack(self) -> None:
        """struct packs/unpacks binary data."""
        packed = struct.pack(">hf", 42, 3.14)
        assert isinstance(packed, bytes)
        short_val, float_val = struct.unpack(">hf", packed)
        assert short_val == 42
        assert abs(float_val - 3.14) < 0.01

    def test_struct_calcsize(self) -> None:
        """struct.calcsize returns the size of a format."""
        assert struct.calcsize(">i") == 4  # 4-byte int
        assert struct.calcsize(">d") == 8  # 8-byte double
        assert struct.calcsize(">hh") == 4  # Two 2-byte shorts
