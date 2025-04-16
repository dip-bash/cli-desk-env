# cli-desk-env
get desktop env like feel in command line interface

## Description

`cli-desk-env` is a command-line interface (CLI) tool designed to emulate a desktop environment within a terminal using `tmux`. It provides an interactive launcher, a customizable panel, and seamless integration with `tmux` to manage programs, windows, and panes efficiently. Whether you're a power user who loves the terminal or someone transitioning from a graphical desktop, this project brings a familiar desktop-like feel to the CLI.

---

## Screenshot

<table style="border-collapse: collapse; width: 100%;">
  <tr>
    <td style="width: 50%; padding: 0; border: none;">
      <img src="https://github.com/dip-bash/img/raw/0d6b7d5263abc5cb9fb3a624d336e8e9081923f3/cli-desk-env/Screenshot%20from%202025-04-01%2017-26-48.png" alt="Screenshot 1" style="max-width: 100%; display: block;">
    </td>
    <td style="width: 50%; padding: 0; border: none;">
      <img src="https://github.com/dip-bash/img/raw/0d6b7d5263abc5cb9fb3a624d336e8e9081923f3/cli-desk-env/Screenshot%20from%202025-04-01%2017-28-14.png" alt="Screenshot 2" style="max-width: 100%; display: block;">
    </td>
  </tr>
</table>

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
git clone https://github.com/dip-bash/cli-desk-env
```
```
cd cli-desk-env
```
```
chmod +x install.sh
```
```
./install.sh
```
```
tmux -u
```
2. Uninstall
```bash
chmod +x uninstall.sh

./uninstall.sh
