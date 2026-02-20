"""Tests for Chapter 17: Networking and Protocols."""

import json
import socket
import threading
import urllib.parse


class TestSocketFundamentals:
    """Test socket basics."""

    def test_tcp_echo_server(self) -> None:
        """TCP client-server communication works."""
        received: list[bytes] = []

        def echo_server(server_sock: socket.socket) -> None:
            conn, _ = server_sock.accept()
            data = conn.recv(1024)
            received.append(data)
            conn.sendall(data)
            conn.close()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        port = server.getsockname()[1]
        server.listen(1)

        t = threading.Thread(target=echo_server, args=(server,))
        t.start()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", port))
        client.sendall(b"Hello, TCP!")
        response = client.recv(1024)
        client.close()
        server.close()
        t.join()

        assert response == b"Hello, TCP!"
        assert received[0] == b"Hello, TCP!"

    def test_udp_communication(self) -> None:
        """UDP send and receive works."""
        received: list[bytes] = []

        def udp_receiver(sock: socket.socket) -> None:
            data, _ = sock.recvfrom(1024)
            received.append(data)

        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(("127.0.0.1", 0))
        port = server.getsockname()[1]

        t = threading.Thread(target=udp_receiver, args=(server,))
        t.start()

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto(b"Hello, UDP!", ("127.0.0.1", port))
        client.close()
        t.join()
        server.close()

        assert received[0] == b"Hello, UDP!"

    def test_socket_address_info(self) -> None:
        """getaddrinfo resolves host and service names."""
        results = socket.getaddrinfo("localhost", None, socket.AF_INET)
        assert len(results) > 0
        assert results[0][0] == socket.AF_INET


class TestURLHandling:
    """Test URL parsing and construction."""

    def test_url_parsing(self) -> None:
        """urllib.parse breaks URLs into components."""
        url = "https://example.com:8080/path?key=value&q=test#section"
        parsed = urllib.parse.urlparse(url)

        assert parsed.scheme == "https"
        assert parsed.hostname == "example.com"
        assert parsed.port == 8080
        assert parsed.path == "/path"
        assert parsed.fragment == "section"

    def test_query_string_parsing(self) -> None:
        """parse_qs extracts query parameters."""
        query = "name=Alice&age=30&tag=python&tag=coding"
        params = urllib.parse.parse_qs(query)

        assert params["name"] == ["Alice"]
        assert params["age"] == ["30"]
        assert params["tag"] == ["python", "coding"]

    def test_url_encoding(self) -> None:
        """urlencode builds query strings from dicts."""
        params = {"name": "Alice Bob", "city": "New York"}
        encoded = urllib.parse.urlencode(params)
        assert "name=Alice+Bob" in encoded
        assert "city=New+York" in encoded


class TestJSONProtocol:
    """Test JSON-based communication patterns."""

    def test_json_request_response(self) -> None:
        """JSON serialization for network messages."""
        request = {"action": "greet", "name": "Alice"}
        encoded: bytes = json.dumps(request).encode("utf-8")

        decoded: dict = json.loads(encoded.decode("utf-8"))
        assert decoded == request
        assert decoded["action"] == "greet"

    def test_json_message_framing(self) -> None:
        """Length-prefixed framing for JSON messages."""
        message = {"type": "chat", "text": "Hello!"}
        payload: bytes = json.dumps(message).encode("utf-8")
        frame: bytes = len(payload).to_bytes(4, "big") + payload

        # Parse the frame
        length = int.from_bytes(frame[:4], "big")
        body = json.loads(frame[4 : 4 + length].decode("utf-8"))
        assert body == message
