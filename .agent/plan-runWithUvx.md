# Plan: Run moomoo_mcp.server with uv / uvx

Goal: install locally, ensure OpenD is available, and run the MCP server using `uv` / `uvx` tooling.

Prerequisites
- macOS, Python 3.10+ (pyproject requires 3.10+).
- Git (repo already present).
- Local OpenD gateway running and reachable at `127.0.0.1:11111`.

High-level steps
1. Create and activate a virtual environment.
2. Install project runtime + dev dependencies in editable mode.
3. (Optional) Install the `uv` / `uvx` CLI if not already present.
4. Verify OpenD is running.
5. Run the MCP server via `uv` or `uvx`.
6. Run tests with `pytest`.

Commands

1) Create venv and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

2) Install uv/uvx CLI (if missing)

The repository README references `uv`/`uvx` tooling. If you don't have these commands available, install them into the venv or via your system package manager. Example (attempt via pip):

```bash
pip install uv
# or, if the project recommends uvx, try:
pip install uvx
```

If `uv`/`uvx` aren't pip packages in your environment, install the tooling you use locally (homebrew, custom script) that exposes `uv`/`uvx` commands.

3) Verify OpenD (must be running before the MCP server)

```bash
# TCP check
nc -vz 127.0.0.1 11111
# or
ss -ltnp | grep 11111
```

4) Run the server via uv / uvx

Preferred run (uses the entry `moomoo-api-mcp = "moomoo_mcp.server:main"` from pyproject):

```bash
# basic: runs installed entrypoint
uv run moomoo-api-mcp

# or refresh/install-and-run (if supported by your uvx tooling):
uvx --refresh moomoo-api-mcp
```

Alternative (no uv/uvx):

```bash
python -m moomoo_mcp.server
```

Env vars (examples)
- Simulation (default): no special envs required.
- REAL (auto-unlock):

```bash
export MOOMOO_TRADE_PASSWORD='your-real-password'
# or
export MOOMOO_TRADE_PASSWORD_MD5='md5-of-password'
export MOOMOO_SECURITY_FIRM='FUTUSG'  # optional
```

Notes / verification
- Watch server logs: it should attempt to connect to `127.0.0.1:11111` and register services.
- If OpenD is not reachable the server will not be able to serve market/trade features.
- Run tests with:

```bash
pytest -q
```

Troubles & tips
- If `uv`/`uvx` command is not found after installation, ensure the venv is active or adjust PATH to the venv `bin` directory.
- If third-party packages fail to install, check PyPI compatibility and try upgrading `pip` or using a different Python minor (3.10/3.11).
- Do not share real trading passwords in chat. Use env vars locally.

Saved by: plan-runWithUvx generator
