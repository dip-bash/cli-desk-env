
import os
import sys
import tty
import termios
import signal
import subprocess
import json
from pathlib import Path

# ANSI Constants
ANSI = {
    "GREEN": "\033[92m",
    "RESET": "\033[0m",
    "CLEAR": "\033[2J\033[H",
}

# Key Constants
KEYS = {
    "LEFT": "\x1b[D",
    "RIGHT": "\x1b[C",
    "ENTER": "\r",
    "ESCAPE": "\x1b",
    "CTRLC": "\x03",
}

# Configuration
CONFIG = {
    "BASH_SCRIPT": Path("~/.config/tmux/select_active.sh").expanduser(),
    "JSON_FILE": Path(__file__).parent / "panel.json"
}

class TerminalContext:
    """Context manager for terminal settings preservation."""
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.original_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.original_settings)

def load_menu_items():
    """Load menu items from JSON configuration file."""
    try:
        with CONFIG["JSON_FILE"].open() as f:
            items = json.load(f)
        return {i+1: item["name"] for i, item in enumerate(items)}
    except FileNotFoundError:
        exit_with_error(f"Configuration file {CONFIG['JSON_FILE']} not found")
    except (json.JSONDecodeError, KeyError) as e:
        exit_with_error(f"Invalid configuration: {str(e)}")

def exit_with_error(message):
    """Print error message and exit with status code 1."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)

def clear_screen():
    """Clear terminal screen using ANSI escape codes."""
    sys.stdout.write(ANSI["CLEAR"])
    sys.stdout.flush()

def display_selection_menu(selected_pos, items):
    """Display interactive selection menu with highlighted option."""
    menu_line = " ".join(
        format_item(i, name, selected_pos)
        for i, name in enumerate(items, 1)
    )
    print(menu_line, end='', flush=True)

def format_item(position, name, selected_pos):
    """Format menu item with proper highlighting."""
    if position == selected_pos:
        return f"{ANSI['GREEN']}[{name.upper()}]{ANSI['RESET']}"
    return f"[{name}]"

def execute_command(program_name, mode):
    """Execute command in specified tmux mode."""
    mode_flag = "--pane" if mode == "pane" else "--window"
    command = f"{CONFIG['BASH_SCRIPT']} {mode_flag} {program_name}"
    
    try:
        subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        pass

def get_user_input():
    """Capture single key input with arrow key support."""
    with TerminalContext():
        key = sys.stdin.read(1)
        if key == '\x1b':
            return handle_escape_sequence()
        return key

def handle_escape_sequence():
    """Process escape sequence for special keys."""
    if sys.stdin.read(1) == '[':
        return f"\x1b[{sys.stdin.read(1)}"
    return KEYS["ESCAPE"]

def main():
    """Main program execution loop."""
    signal.signal(signal.SIGINT, lambda *_: exit_with_error("User interrupt"))
    
    if not CONFIG["BASH_SCRIPT"].exists():
        exit_with_error(f"Missing script: {CONFIG['BASH_SCRIPT']}")

    menu_items = load_menu_items()
    selected_program = 1
    current_mode = "main"  # or "submenu"
    submenu_items = ["pane", "window"]
    selected_submenu = 1

    while True:
        clear_screen()
        
        if current_mode == "main":
            display_selection_menu(selected_program, list(menu_items.values()))
        elif current_mode == "submenu":
            # Show program name and submenu
            program_name = menu_items[selected_program]
            print(f"{program_name}: ", end='')
            display_selection_menu(selected_submenu, submenu_items)
        
        user_input = get_user_input()

        if current_mode == "main":
            if user_input in (KEYS["LEFT"], KEYS["RIGHT"]):
                selected_program = handle_navigation(
                    user_input, selected_program, len(menu_items))
            elif user_input == KEYS["ENTER"]:
                current_mode = "submenu"
            elif user_input == KEYS["ESCAPE"]:
                clear_screen()
                print("Exiting program...")
                break
            elif user_input.isdigit():
                if (choice := int(user_input)) in menu_items:
                    execute_command(menu_items[choice], "pane")
        
        elif current_mode == "submenu":
            if user_input in (KEYS["LEFT"], KEYS["RIGHT"]):
                selected_submenu = handle_navigation(
                    user_input, selected_submenu, len(submenu_items))
            elif user_input == KEYS["ENTER"]:
                mode = submenu_items[selected_submenu - 1]
                execute_command(menu_items[selected_program], mode)
                current_mode = "main"
            elif user_input == KEYS["ESCAPE"]:
                current_mode = "main"

def handle_navigation(key, current_pos, item_count):
    """Update selection position based on navigation keys."""
    if key == KEYS["LEFT"]:
        return max(1, current_pos - 1)
    if key == KEYS["RIGHT"]:
        return min(item_count, current_pos + 1)
    return current_pos

if __name__ == "__main__":
    main()