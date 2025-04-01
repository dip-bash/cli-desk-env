# cli-desk-env
get desktop env like feel in command line interface

## Description

`cli-desk-env` is a command-line interface (CLI) tool designed to emulate a desktop environment within a terminal using `tmux`. It provides an interactive launcher, a customizable panel, and seamless integration with `tmux` to manage programs, windows, and panes efficiently. Whether you're a power user who loves the terminal or someone transitioning from a graphical desktop, this project brings a familiar desktop-like feel to the CLI.

---
![image alt](https://github.com/dip-bash/img/blob/0d6b7d5263abc5cb9fb3a624d336e8e9081923f3/cli-desk-env/Screenshot%20from%202025-04-01%2017-26-48.png)

<img src="https://github.com/dip-bash/img/blob/0d6b7d5263abc5cb9fb3a624d336e8e9081923f3/cli-desk-env/Screenshot%20from%202025-04-01%2017-26-48.png" alt="Image 1 Description" style="width: 49%; margin-right: 1%; display: inline-block;">
<img src="https://github.com/dip-bash/img/blob/0d6b7d5263abc5cb9fb3a624d336e8e9081923f3/cli-desk-env/Screenshot%20from%202025-04-01%2017-28-14.png" alt="Image 2 Description" style="width: 49%; display: inline-block;">
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
- Bash
- Linux GNOME environment (optional)

## Installation

1. Install
```bash
git clone https://github.com/dip-bash/cli_desktop_proto.git
```
```
cd cli_desktop_proto
```
```
chmod +x install.sh
```
```
./install.sh
```
```
tmux
```
2. Uninstall
```bash
chmod +x uninstall.sh

./uninstall.sh
