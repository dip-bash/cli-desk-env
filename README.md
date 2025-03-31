# cli-desk-env
get desktop env like feel in command line interface

## Description

`cli-desk-env` is a command-line interface (CLI) tool designed to emulate a desktop environment within a terminal using `tmux`. It provides an interactive launcher, a customizable panel, and seamless integration with `tmux` to manage programs, windows, and panes efficiently. Whether you're a power user who loves the terminal or someone transitioning from a graphical desktop, this project brings a familiar desktop-like feel to the CLI.

---
## Features

### Tmux Configuration
- **Application Launcher** (F2): launch applications
- **System Panel** (F3): Quick-access menu for common utilities
- **Tmux Integration**: Enhanced window/pane management
- **JSON Configuration**: Easy-to-modify program definitions
- **Battery/Clock Display**: Status bar with system info

- Custom prefix (Ctrl-a)
- Mouse support
- Top status bar with time, date, and session info
- Easy window and pane management
- VI-style copy mode
- Custom key bindings:
  - F1: Terminal popup
  - Intuitive pane navigation and resizing
- you can read more shorcuts in `SHORTCUTS.md` file
  


## Technologies Used
- Tmux (Terminal Multiplexer)
- Python 3
- Bash (installation script)
- Linux GNOME environment

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dip-bash/cli_desktop_proto.git

cd cli_desktop_proto

chmod +x install.sh

# Install with dependency management
./install.sh

# Force reinstall dependencies (add to script options)
./install.sh --force-deps

tmux
