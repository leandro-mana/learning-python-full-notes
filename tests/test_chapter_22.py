"""Tests for Chapter 22: Web Development Fundamentals."""

import http
import json
from urllib.parse import parse_qs, urlencode


class TestHTTPConcepts:
    """Test HTTP fundamentals."""

    def test_http_status_codes(self) -> None:
        """HTTPStatus provides standard status codes."""
        assert http.HTTPStatus.OK == 200
        assert http.HTTPStatus.NOT_FOUND == 404
        assert http.HTTPStatus.INTERNAL_SERVER_ERROR == 500
        assert http.HTTPStatus.OK.phrase == "OK"

    def test_http_methods(self) -> None:
        """Standard HTTP methods are well-defined strings."""
        methods = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
        assert "GET" in methods
        assert "POST" in methods


class TestWSGI:
    """Test WSGI concepts."""

    def test_wsgi_app_callable(self) -> None:
        """A WSGI app is a callable that takes environ and start_response."""
        responses: list[tuple[str, list]] = []

        def start_response(status: str, headers: list) -> None:
            responses.append((status, headers))

        def app(environ: dict, start_response) -> list[bytes]:
            start_response("200 OK", [("Content-Type", "text/plain")])
            return [b"Hello, World!"]

        environ = {"REQUEST_METHOD": "GET", "PATH_INFO": "/"}
        body = app(environ, start_response)

        assert body == [b"Hello, World!"]
        assert responses[0][0] == "200 OK"

    def test_wsgi_environ_keys(self) -> None:
        """WSGI environ contains standard CGI variables."""
        environ = {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/api/users",
            "QUERY_STRING": "page=1&limit=10",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "8000",
        }
        assert environ["REQUEST_METHOD"] == "GET"
        assert environ["PATH_INFO"] == "/api/users"
        params = parse_qs(environ["QUERY_STRING"])
        assert params["page"] == ["1"]


class TestRouting:
    """Test URL routing patterns."""

    def test_simple_router(self) -> None:
        """A router maps URL paths to handler functions."""
        routes: dict[str, callable] = {}

        def route(path: str):
            def decorator(func):
                routes[path] = func
                return func

            return decorator

        @route("/")
        def index() -> str:
            return "Home"

        @route("/about")
        def about() -> str:
            return "About"

        assert routes["/"]() == "Home"
        assert routes["/about"]() == "About"
        assert "/missing" not in routes

    def test_json_response_building(self) -> None:
        """JSON responses combine status, headers, and body."""
        data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
        body: bytes = json.dumps(data).encode("utf-8")
        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
        ]

        assert json.loads(body) == data
        assert any(k == "Content-Type" for k, v in headers)


class TestFormHandling:
    """Test form data processing."""

    def test_url_encoded_form_data(self) -> None:
        """URL-encoded form data is parsed with parse_qs."""
        form_data = "username=alice&password=secret123&remember=on"
        parsed = parse_qs(form_data)

        assert parsed["username"] == ["alice"]
        assert parsed["password"] == ["secret123"]
        assert parsed["remember"] == ["on"]

    def test_form_data_encoding(self) -> None:
        """urlencode builds form-encoded strings from dicts."""
        data = {"name": "Alice Bob", "email": "alice@example.com"}
        encoded = urlencode(data)
        assert "name=Alice+Bob" in encoded
        assert "email=alice%40example.com" in encoded
