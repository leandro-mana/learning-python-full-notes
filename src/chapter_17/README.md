# Chapter 17: Networking and Protocols

## Topics Covered
- Socket programming: TCP and UDP clients/servers
- `socket` module: `AF_INET`, `SOCK_STREAM`, `SOCK_DGRAM`
- HTTP with `urllib.request` and `http.client`
- `json` over HTTP: REST-style patterns
- `asyncio` networking: streams, protocols, transports
- `socketserver` for concurrent servers (threading/forking)
- SSL/TLS with `ssl` module
- Network error handling and timeouts

## Notebooks
1. **01_socket_fundamentals.ipynb** — TCP/UDP clients and servers, socket options
2. **02_http_and_urls.ipynb** — urllib, http.client, REST patterns, JSON APIs
3. **03_async_networking.ipynb** — asyncio streams, concurrent connections, SSL

## Key Takeaways
- Sockets are the foundation of all network communication
- Use higher-level abstractions (urllib, asyncio) for production code
- Always handle timeouts, connection errors, and partial reads
- asyncio enables high-concurrency networking without threads
