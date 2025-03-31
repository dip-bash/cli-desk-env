#!/bin/bash

# Debug function to print messages
debug() {
    echo "[DEBUG] $1" >&2
}

# Check for required arguments
if [ $# -lt 2 ]; then
    debug "Usage: $0 [--pane|--window] <program>"
    exit 1
fi

MODE="$1"
PROGRAM="$2"

# Check if tmux is running
if ! tmux has-session >/dev/null 2>&1; then
    debug "No tmux session running. Starting new session..."
    tmux new-session -d
fi

# Get session information
SESSION=$(tmux display-message -p '#S')
WINDOW=$(tmux display-message -p '#I')
debug "Current session: $SESSION, window: $WINDOW"

case $MODE in
    --pane)
        # Split current window horizontally
        debug "Creating new pane with: $PROGRAM"
        tmux split-window -h -c "#{pane_current_path}" "$PROGRAM"
        ;;
    --window)
        # Check if current window has active processes (excluding shell)
        if tmux list-panes -F "#{pane_active}:#{pane_current_command}" | grep -vq "1:bash"; then
            debug "Creating new window for: $PROGRAM"
            tmux new-window -c "#{pane_current_path}" "$PROGRAM"
        else
            debug "Reusing current window for: $PROGRAM"
            tmux send-keys "$PROGRAM" C-m
        fi
        ;;
    *)
        debug "Invalid mode: $MODE"
        exit 1
        ;;
esac