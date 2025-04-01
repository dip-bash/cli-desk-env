import os
import sys
import shutil
import json
import curses
import subprocess

# --------------------------------------------
# Load Tools Configuration
# --------------------------------------------
config_path = os.path.expanduser('~/.config/tmux/programs.json')
tools_dict = {}
if os.path.exists(config_path):
    try:
        with open(config_path, 'r') as f:
            tools_dict = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {config_path}")
        exit(1)
else:
    print(f"Error: Config file not found at {config_path}")
    exit(1)

# --------------------------------------------
# Matching Functions
# --------------------------------------------
def get_top_matches(search_term, limit=9):
    """
    Return tools that match the search term using case-insensitive substring matching.
    Each match is assigned a basic score.
    """
    matches = []
    search_term_lower = search_term.lower()
    for tool in tools_dict.keys():
        tool_lower = tool.lower()
        if not search_term or search_term_lower in tool_lower:
            score = 100 if search_term_lower == tool_lower else 50
            matches.append((tool, score))
    matches.sort(key=lambda x: (-x[1], x[0]))
    return matches[:limit]

# --------------------------------------------
# Curses Helper for Highlighting Search Matches
# --------------------------------------------
def draw_highlighted_string(win, y, x, text, search_term):
    """
    Draws text on window 'win' starting at (y, x). If the search term appears 
    (case-insensitive) within the text, that substring is highlighted in red.
    """
    if not search_term:
        win.addstr(y, x, text)
        return

    search_lower = search_term.lower()
    text_lower = text.lower()
    pos = text_lower.find(search_lower)
    if pos == -1:
        win.addstr(y, x, text)
        return

    # Print text before match.
    win.addstr(y, x, text[:pos])
    x += pos
    # Print the matched segment with the red highlight color.
    win.addstr(y, x, text[pos:pos+len(search_term)], curses.color_pair(1))
    x += len(search_term)
    # Print the remainder.
    win.addstr(y, x, text[pos+len(search_term):])

# --------------------------------------------
# Main Curses Application Function
# --------------------------------------------
def curses_main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_CYAN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)

    search_term = ""

    while True:
        stdscr.clear()
        # Display header information.
        stdscr.addstr(0, 0, "Tool Search (Press Ctrl+C to exit)", curses.color_pair(4))
        stdscr.addstr(1, 0, "Current search: " + search_term, curses.color_pair(4))

        # Retrieve matching tools.
        matches = get_top_matches(search_term)

        # Table dimensions and border.
        table_start = 3
        index_width = 6
        tool_width = 20
        command_width = 40
        total_width = index_width + tool_width + command_width + 2
        border = "=" * total_width

        # Draw table header.
        stdscr.addstr(table_start, 0, border, curses.color_pair(2))
        header_str = f"{'Index':<{index_width}} {'Tool Name':<{tool_width}} {'Command':<{command_width}}"
        stdscr.addstr(table_start + 1, 0, header_str, curses.color_pair(2))
        stdscr.addstr(table_start + 2, 0, border, curses.color_pair(2))

        # Draw table rows.
        for idx, (tool, _) in enumerate(matches, 1):
            row = table_start + 2 + idx
            index_str = f"{idx})"
            stdscr.addstr(row, 0, index_str.ljust(index_width), curses.color_pair(3))
            x_tool = index_width + 1
            tool_display = tool[:tool_width]  
            draw_highlighted_string(stdscr, row, x_tool, tool_display, search_term)
            x_cmd = x_tool + tool_width + 1
            command = tools_dict[tool]["command"]
            command_display = command[:command_width]
            stdscr.addstr(row, x_cmd, command_display)
        # Draw bottom border.
        stdscr.addstr(table_start + len(matches) + 3, 0, border, curses.color_pair(2))

        # Display prompt at the bottom.
        prompt_line = table_start + len(matches) + 5
        stdscr.addstr(prompt_line, 0, 
            "Enter number to execute, type to search, or press Backspace to delete", curses.color_pair(5))

        stdscr.refresh()

        # Wait for user input.
        key = stdscr.getch()

        # Use Ctrl+C for exit.
        if key == 3:  # ASCII 3 is Ctrl+C.
            break

        # If key represents a digit, execute the corresponding tool.
        if 48 <= key <= 57:
            digit = key - 48
            if digit > 0 and digit <= len(matches):
                selected_tool = matches[digit - 1][0]
                tool_info = tools_dict[selected_tool]
                command = tool_info["command"]
                foreground = tool_info["foreground"]
                command_base = command.split()[0]
                if shutil.which(command_base):
                    # End curses mode before executing the command.
                    curses.endwin()
                    if foreground:
                        subprocess.run(command, shell=True)
                    else:
                        subprocess.Popen(command, shell=True)
                    return
                else:
                    stdscr.addstr(prompt_line + 2, 0, 
                        f"Error: Command '{command_base}' not found in PATH.", curses.color_pair(1))
                    stdscr.refresh()
                    stdscr.getch()
        # Handle Backspace key for deleting a character.
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            search_term = search_term[:-1]
        # Append printable characters to the search term.
        elif 32 <= key <= 126:
            search_term += chr(key)

# --------------------------------------------
# Application Entry Point
# --------------------------------------------
def main():
    try:
        curses.wrapper(curses_main)
    except KeyboardInterrupt:
        curses.endwin()
        sys.exit(0)

if __name__ == "__main__":
    main()
