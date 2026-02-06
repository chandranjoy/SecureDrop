#!/bin/bash

APP_NAME="securedrop"
APP_DIR="/opt/securedrop/backend"
VENV_DIR="/opt/securedrop/.venv"
LOG_DIR="/var/log"
LOG_FILE="/var/log/securedrop.log"
PID_FILE="/var/run/securedrop.pid"

HOST="0.0.0.0"
PORT="8080"

UVICORN_CMD="$VENV_DIR/bin/uvicorn app.main:app --host $HOST --port $PORT"

mkdir -p "$LOG_DIR"
touch "$LOG_FILE"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

start() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
        log "START requested but app already running (PID $(cat $PID_FILE))"
        echo "Already running"
        exit 0
    fi

    log "Starting $APP_NAME..."
    cd "$APP_DIR" || exit 1
    source "$VENV_DIR/bin/activate"

    nohup $UVICORN_CMD >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"

    sleep 2

    if kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
        log "Started successfully (PID $(cat $PID_FILE))"
        echo "Started"
    else
        log "Failed to start"
        echo "Failed to start"
        rm -f "$PID_FILE"
    fi
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        log "STOP requested but PID file not found"
        echo "Not running"
        return
    fi

    PID=$(cat "$PID_FILE")

    if kill -0 "$PID" 2>/dev/null; then
        log "Stopping $APP_NAME (PID $PID)..."
        kill "$PID"

        for i in {1..10}; do
            if kill -0 "$PID" 2>/dev/null; then
                sleep 1
            else
                break
            fi
        done

        if kill -0 "$PID" 2>/dev/null; then
            log "Force killing $APP_NAME (PID $PID)"
            kill -9 "$PID"
        fi

        log "Stopped"
        rm -f "$PID_FILE"
        echo "Stopped"
    else
        log "Stale PID file found, cleaning up"
        rm -f "$PID_FILE"
        echo "Not running"
    fi
}

restart() {
    log "Restart requested"
    stop
    start
}

status() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
        echo "Running (PID $(cat $PID_FILE))"
    else
        echo "Stopped"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
