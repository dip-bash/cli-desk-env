# Tmux Shortcuts

This document lists all shortcuts available with the provided `tmux.conf` configuration, as well as default tmux shortcuts that remain functional because they are not overridden.

## General
- **Prefix**: `Ctrl-a` (replaces default `Ctrl-b`)
- `Ctrl-a Ctrl-a` - Send the prefix to the underlying application (e.g., nested tmux sessions).

## Session Management
- `Ctrl-a S` - Choose a session from a list.
- `Ctrl-a D` - Detach from the current session.
- **Default Available**:
  - `Ctrl-a s` - List sessions (similar to `choose-session`, but default style).
  - `Ctrl-a $` - Rename the current session.

## Window Management
- `Ctrl-a c` - Create a new window (starts in current pane's path).
- `Ctrl-a n` - Switch to the next window.
- `Ctrl-a p` - Switch to the previous window.
- `Ctrl-a X` - Kill the current window.
- `Ctrl-a 1-9` - Switch to window number 1-9 (starts at 1 due to `base-index 1`).
- **Default Available**:
  - `Ctrl-a ,` - Rename the current window.
  - `Ctrl-a &` - Kill the current window (alternative to `X`).
  - `Ctrl-a 0` - Switch to window 0 (though less useful with `base-index 1`).
  - `Ctrl-a l` - Switch to the last window (not overridden by pane navigation).

## Pane Management
- `Ctrl-a ;` - Split window horizontally.
- `Ctrl-a '` - Split window vertically.
- `Ctrl-a x` - Kill the current pane.
- `Ctrl-a Tab` - Cycle to the next pane.
- **Pane Navigation**:
  - `Ctrl-a h` - Move to the left pane.
  - `Ctrl-a j` - Move to the down pane.
  - `Ctrl-a k` - Move to the up pane.
  - `Ctrl-a l` - Move to the right pane.
- **Pane Resizing**:
  - `Ctrl-a H` - Resize pane left by 5 cells.
  - `Ctrl-a J` - Resize pane down by 5 cells.
  - `Ctrl-a K` - Resize pane up by 5 cells.
  - `Ctrl-a L` - Resize pane right by 5 cells.
- **Default Available**:
  - `Ctrl-a %` - Split window horizontally (alternative to `;`).
  - `Ctrl-a "` - Split window vertically (alternative to `'`).
  - `Ctrl-a o` - Rotate through panes (alternative to `Tab`).
  - `Ctrl-a q` - Briefly display pane numbers.
  - `Ctrl-a z` - Toggle pane zoom (full-screen current pane).
  - `Ctrl-a !` - Convert pane into a new window.

## Copy Mode (VI-style)
- `Ctrl-a [` - Enter copy mode.
- **In Copy Mode**:
  - `v` - Begin selection.
  - `y` - Copy selection and exit copy mode.
  - Uses VI navigation keys (e.g., `h`, `j`, `k`, `l`) due to `set -g mode-keys vi`.
- **Default Available**:
  - `Ctrl-a ]` - Paste the most recent buffer.

## Configuration
- `Ctrl-a r` - Reload the tmux configuration file (`~/.tmux.conf`).

## Custom Shortcuts
- `F1` - Open a centered popup terminal (80% width/height) in the current pane's directory.
- `F2` - Run the `launcher.py` script in the current pane.
- `F3` - Open Quick-access menu 

## Mouse Support
- Enabled with `set -g mouse on`:
  - **Click** - Select panes or windows in the status bar.
  - **Scroll** - Enter copy mode and navigate history.
  - **Drag** - Resize panes.

## Additional Default Shortcuts
These are standard tmux shortcuts that remain available as they aren’t overridden:
- `Ctrl-a :` - Enter command mode (e.g., type `new-session`).
- `Ctrl-a ?` - List all key bindings (tmux help).
- `Ctrl-a t` - Show a clock in the current pane.
- `Ctrl-a w` - Choose a window from a list.
- `Ctrl-a f` - Find a window by name.
- `Ctrl-a .` - Move the current window to a new index.
- `Ctrl-a #` - List all paste buffers.
- `Ctrl-a =` - Choose a paste buffer to paste.
- `Ctrl-a d` - Detach the current client (lowercase `d`, differs from `D` slightly in multi-client scenarios).

## Notes
- Shortcuts marked as **Default Available** are part of tmux’s default bindings and work unless explicitly unbound or overridden.
- The `Ctrl-a l` binding for pane navigation overrides the default "last window" binding, but you can still access the last window with other methods (e.g., `Ctrl-a n`/`p`).
- Mouse interactions complement keyboard shortcuts when `mouse on` is enabled.
