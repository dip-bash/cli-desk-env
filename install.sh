#!/bin/bash

set -euo pipefail

# Configuration variables
TARGET_DIR="$HOME/.config/tmux"
BACKUP_DIR="$TARGET_DIR/backup"
FILES=("launcher.py" "panel.json" "panel.py" "programs.json" "select_active.sh" "tmux.conf")

# Check if all required files exist in current directory
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "Error: Required file $file not found in current directory. Aborting."
        exit 1
    fi
done

# Check for existing files
EXISTING_FILES=()
for file in "${FILES[@]}"; do
    if [ -e "$TARGET_DIR/$file" ]; then
        EXISTING_FILES+=("$file")
    fi
done

# Handle existing files
if [ ${#EXISTING_FILES[@]} -gt 0 ]; then
    echo "The following files already exist in $TARGET_DIR:"
    printf "• %s\n" "${EXISTING_FILES[@]}"
    echo "Choose an option:"
    echo "1) Backup existing files and install new ones"
    echo "2) Replace existing files without backup"
    echo "3) Skip existing files (install only new ones)"
    read -p "Enter your choice [1-3]: " choice

    case $choice in
        1)
            echo "Backing up existing files to $BACKUP_DIR..."
            mkdir -p "$BACKUP_DIR"
            for file in "${EXISTING_FILES[@]}"; do
                backup_file="$BACKUP_DIR/${file}.backup"
                if [ -e "$backup_file" ]; then
                    echo "Overwriting previous backup: $backup_file"
                fi
                mv -v "$TARGET_DIR/$file" "$backup_file"
            done
            ;;
        2)
            echo "Replacing existing files..."
            for file in "${EXISTING_FILES[@]}"; do
                rm -v "$TARGET_DIR/$file"
            done
            ;;
        3)
            echo "Skipping existing files..."
            # Remove existing files from files array
            for existing_file in "${EXISTING_FILES[@]}"; do
                for i in "${!FILES[@]}"; do
                    if [[ "${FILES[i]}" == "$existing_file" ]]; then
                        unset 'FILES[i]'
                    fi
                done
            done
            # Rebuild array to remove empty indices
            FILES=("${FILES[@]}")
            ;;
        *)
            echo "Invalid choice. Aborting installation."
            exit 1
            ;;
    esac
fi

# Install files
echo "Installing files to $TARGET_DIR..."
mkdir -p "$TARGET_DIR"
for file in "${FILES[@]}"; do
    cp -v "$file" "$TARGET_DIR/$file"
done

# Make .sh files executable
for file in "${FILES[@]}"; do
    if [[ $file == *.sh ]]; then
        chmod +x "$TARGET_DIR/$file"
        echo "Made executable: $TARGET_DIR/$file"
    fi
done

echo "Installation complete!"
