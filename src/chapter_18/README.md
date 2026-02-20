# Chapter 18: Database Access

## Topics Covered
- `sqlite3` module: connections, cursors, queries
- DB-API 2.0 (PEP 249): the standard database interface
- Parameterized queries and SQL injection prevention
- Transactions: commit, rollback, autocommit, context managers
- Schema design and migrations
- Row factories and custom types
- In-memory databases for testing
- ORM patterns and the Repository pattern

## Notebooks
1. **01_sqlite3_fundamentals.ipynb** — Connections, CRUD, parameterized queries
2. **02_transactions_and_patterns.ipynb** — Transactions, context managers, row factories
3. **03_advanced_database.ipynb** — Migrations, testing patterns, repository pattern

## Key Takeaways
- Always use parameterized queries to prevent SQL injection
- Context managers ensure proper transaction handling
- In-memory databases make tests fast and isolated
- The Repository pattern decouples business logic from data access
