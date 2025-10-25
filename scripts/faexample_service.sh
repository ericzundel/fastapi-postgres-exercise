#!/usr/bin/env bash
# This script starts the FastAPI application using Uvicorn and writes out it's pid to a 
# file for later management.

set -euo pipefail  # Exit on error, undefined vars, and pipeline failures

if [ $# -eq 0 ]; then
    echo "Error: No command provided."
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
fi

# Get the root of the workspace, ignoring $CWD
WORKSPACE_ROOT=$(dirname "$(realpath "$0")")/..
cd ${WORKSPACE_ROOT}

# Source the shared libraries
source "${WORKSPACE_ROOT}/scripts/lib/cli_utils.sh"

APP="app.main:app"
HOST="0.0.0.0"
PORT=8000
PIDDIR="./run"
LOGDIR="./logs"
if [ ! -d "$PIDDIR" ]; then
    mkdir -p "$PIDDIR"
fi

if [ ! -d "$LOGDIR" ]; then
    mkdir -p "$LOGDIR"
fi

PIDFILE="$PIDDIR/faexample.pid"
LOGFILE="$LOGDIR/faexample.log"

start() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat $PIDFILE)" 2>/dev/null; then
        echo "Uvicorn already running (PID $(cat $PIDFILE))"
        exit 0
    fi

    echo "Starting Uvicorn..."
    nohup uvicorn "$APP" --host "$HOST" --port "$PORT" >> "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    echo "Uvicorn started with PID $(cat $PIDFILE)"
}

stop() {
    if [ ! -f "$PIDFILE" ]; then
        echo "No PID file found — is Uvicorn running?"
        exit 0
    fi

    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Stopping Uvicorn (PID $PID)..."
        kill "$PID"
        rm -f "$PIDFILE"
        echo "Stopped."
    else
        echo "Process not found — cleaning up stale PID file."
        rm -f "$PIDFILE"
    fi
}

status() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat $PIDFILE)" 2>/dev/null; then
        echo "Uvicorn is running (PID $(cat $PIDFILE))"
    else
        echo "Uvicorn is not running"
    fi
}

case "$1" in
    start) start ;;
    stop) stop ;;
    status) status ;;
    restart)
        stop
        sleep 1
        start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac