
# import os
# import sys
# import shutil
# import json

# # Load tools from JSON file
# config_path = os.path.expanduser('~/.config/tmux/programs.json')
# try:
#     with open(config_path, 'r') as f:
#         tools_dict = json.load(f)
# except FileNotFoundError:
#     print(f"Error: Config file not found at {config_path}")
#     exit(1)
# except json.JSONDecodeError:
#     print(f"Error: Invalid JSON format in {config_path}")
#     exit(1)


# def get_top_matches(search_term, limit=9):
#     """Get top matching tools based on search term using basic string matching"""
#     matches = []
#     search_term = search_term.lower()
    
#     for tool in tools_dict.keys():
#         tool_lower = tool.lower()
#         if not search_term or search_term in tool_lower:
#             score = 100 if search_term == tool_lower else (50 if search_term in tool_lower else 0)
#             matches.append((tool, score))
    
#     matches.sort(key=lambda x: (-x[1], x[0]))
#     return matches[:limit]

# def clear_screen():
#     """Clear the console screen"""
#     os.system('clear')

# def main():
#     search_term = ""
    
#     while True:
#         clear_screen()
#         print("Tool Search (Press Ctrl+C to exit)")
#         print(f"Current search: {search_term}")
#         print("\nMatching tools:")
        
#         matches = get_top_matches(search_term)
#         if matches:
#             for i, (tool, _) in enumerate(matches, 1):
#                 print(f"{i}. {tool} - {tools_dict[tool]['command']}")
#         else:
#             print("No matches found")
        
#         print("\nEnter number to execute, continue typing tool name, or use Backspace to delete")
        
#         # Get single character input without requiring Enter (Linux version only)
#         try:
#             import termios
#             import tty
            
#             fd = sys.stdin.fileno()
#             old_settings = termios.tcgetattr(fd)
#             try:
#                 tty.setraw(fd)
#                 char = sys.stdin.read(1)
#             finally:
#                 termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
#             # Handle input
#             if char.isdigit() and 1 <= int(char) <= len(matches):
#                 selected_tool = matches[int(char) - 1][0]
#                 tool_info = tools_dict[selected_tool]
#                 command = tool_info["command"]
#                 foreground = tool_info["foreground"]
#                 clear_screen()
                
#                 # Check if the command exists in PATH
#                 command_base = command.split()[0]
#                 if shutil.which(command_base):
#                     if foreground:
#                         # Run in foreground for terminal-based tools
#                         os.system(command)
#                         return  # Exit after the command finishes
#                     else:
#                         # Run in background for GUI tools
#                         os.system(f"{command} &")
#                         return  # Exit after launching
#                 else:
#                     return  # Silently exit if command not found
#             elif char == '\x03':  # Ctrl+C
#                 break
#             elif char == '\x08' or char == '\x7f':  # Backspace
#                 if search_term:
#                     search_term = search_term[:-1]
#             else:
#                 search_term += char
                
#         except KeyboardInterrupt:
#             break
#         except Exception:
#             break

#     clear_screen()
#     print("Goodbye!")

# if __name__ == "__main__":
#     main()

import os
import sys
import shutil
import json

# Load tools from JSON file
config_path = os.path.expanduser('~/.config/tmux/programs.json')
with open(config_path, 'r') as f:
    tools_dict = json.load(f)

def get_top_matches(search_term, limit=9):
    """Get top matching tools based on search term using basic string matching"""
    matches = []
    search_term = search_term.lower()
    
    for tool in tools_dict.keys():
        tool_lower = tool.lower()
        if not search_term or search_term in tool_lower:
            score = 100 if search_term == tool_lower else (50 if search_term in tool_lower else 0)
            matches.append((tool, score))
    
    matches.sort(key=lambda x: (-x[1], x[0]))
    return matches[:limit]

def clear_screen():
    """Clear the console screen"""
    os.system('clear')

def main():
    search_term = ""
    
    while True:
        clear_screen()
        print(f"Current search: {search_term}")
        
        matches = get_top_matches(search_term)
        if matches:
            for i, (tool, _) in enumerate(matches, 1):
                print(f"{i}. {tool} - {tools_dict[tool]['command']}")
        else:
            print("No matches found")
        
        # Get single character input without requiring Enter (Linux version only)
        try:
            import termios
            import tty
            
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                char = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
            # Handle input
            if char.isdigit() and 1 <= int(char) <= len(matches):
                selected_tool = matches[int(char) - 1][0]
                tool_info = tools_dict[selected_tool]
                command = tool_info["command"]
                foreground = tool_info["foreground"]
                clear_screen()
                
                # Check if the command exists in PATH
                command_base = command.split()[0]
                if shutil.which(command_base):
                    if foreground:
                        os.system(command)
                        return
                    else:
                        os.system(f"{command} &")
                        return
                else:
                    return
            elif char == '\x03':  # Ctrl+C
                break
            elif char == '\x08' or char == '\x7f':  # Backspace
                if search_term:
                    search_term = search_term[:-1]
            else:
                search_term += char
                
        except KeyboardInterrupt:
            break
        except Exception:
            break

    clear_screen()

if __name__ == "__main__":
    main()