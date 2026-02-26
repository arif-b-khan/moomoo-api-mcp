Environment variables and .env usage
===================================

This project reads configuration from environment variables at startup. For convenience during local development you can store variables in a `.env` file at the repository root. The server will load `.env` automatically if present.

Supported variables (relevant to trading):

- `MOOMOO_TRADE_PASSWORD` — Plain-text trade password used to unlock trading on startup. If set, the server will call `unlock_trade` and enable REAL account access.
- `MOOMOO_TRADE_PASSWORD_MD5` — MD5 hash of the password. If provided and `MOOMOO_TRADE_PASSWORD` is not, the server will attempt unlock using the MD5 value.
- `MOOMOO_SECURITY_FIRM` — Optional security firm code used by `TradeService`.

Security notes
--------------
- Do NOT commit a real `.env` to source control. Use `.env.example` as a template and add `.env` to `.gitignore`.
- Use OS or secrets manager in production (Docker secrets, Kubernetes secrets, cloud secret stores, CI secrets).

Example `.env` (local development)

MOOMOO_TRADE_PASSWORD=supersecret

How the server uses .env
------------------------
The MCP server calls a small loader at startup which reads `.env` from the repository root and sets any variables that are not already present in the environment. This allows you to run the server locally using:

```bash
source .venv/bin/activate
# create .env with MOOMOO_TRADE_PASSWORD
PYTHONPATH=src python -m moomoo_mcp.server
```
