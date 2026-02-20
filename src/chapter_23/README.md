# Chapter 23: Security and Cryptography

## Topics Covered
- `hashlib`: SHA-256, MD5, BLAKE2, file hashing
- `hmac`: message authentication codes
- `secrets`: cryptographically secure random values
- Password hashing and verification patterns
- Input validation and sanitization
- Common vulnerabilities: injection, XSS concepts
- `ssl` module basics and certificate verification
- Secure coding principles

## Notebooks
1. **01_hashing_and_hmac.ipynb** — hashlib, HMAC, file integrity, password hashing
2. **02_secrets_and_tokens.ipynb** — secrets module, token generation, secure random
3. **03_secure_coding.ipynb** — Input validation, common vulnerabilities, SSL basics

## Key Takeaways
- Never store passwords in plain text — use proper hashing
- Use `secrets` module for tokens, not `random`
- HMAC provides message integrity and authentication
- Validate all input at system boundaries
