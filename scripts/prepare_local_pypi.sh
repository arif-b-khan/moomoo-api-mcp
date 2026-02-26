#!/usr/bin/env bash
set -euo pipefail

# prepare_local_pypi.sh
# Builds the project wheel into local_pypi/dist and starts a simple HTTP server
# Usage: ./scripts/prepare_local_pypi.sh [port]

PORT=${1:-8081}
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$ROOT_DIR/local_pypi/dist"

echo "Using project root: $ROOT_DIR"

if [ -n "${VIRTUAL_ENV-}" ]; then
  echo "Using active virtualenv: $VIRTUAL_ENV"
else
  echo "No virtualenv detected. It's recommended to run inside .venv."
fi

echo "Ensuring build tool is available..."
python -m pip install --upgrade build >/dev/null

echo "Cleaning previous local_pypi..."
rm -rf "$ROOT_DIR/local_pypi"
mkdir -p "$DIST_DIR"

echo "Building wheel into $DIST_DIR"
PYTHONPATH=src python -m build -w -o "$DIST_DIR"

echo "Wheels produced:"
ls -la "$DIST_DIR"

echo "Starting simple HTTP server on port $PORT serving $ROOT_DIR/local_pypi"
pushd "$ROOT_DIR" >/dev/null
nohup python -m http.server "$PORT" --directory "local_pypi" > local_pypi/server.log 2>&1 &
SERVER_PID=$!
popd >/dev/null

echo "$SERVER_PID" > "$ROOT_DIR/local_pypi/server.pid"
echo "Server started (PID $SERVER_PID). Logs: $ROOT_DIR/local_pypi/server.log"

echo
echo "To install the package from this local index, run (on the same machine):"
WHEEL_NAME=$(basename "$DIST_DIR"/*.whl)
echo "pip install --no-deps --index-url http://localhost:${PORT}/ ${WHEEL_NAME} --trusted-host localhost"
echo
echo "To stop the server: kill $SERVER_PID or rm $ROOT_DIR/local_pypi/server.pid and kill the PID"
