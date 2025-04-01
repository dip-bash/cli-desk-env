#!/bin/bash

set -euo pipefail

# =====================
# Configuration Section
# =====================
TARGET_DIR="$HOME/.config/tmux"
BACKUP_DIR="$TARGET_DIR/backup"
FILES=("launcher.py" "panel.json" "panel.py" "programs.json" "select_active.sh" "tmux.conf")
declare -A DEPENDENCIES=(
    ["python3"]="python3 python3 python python3"
    ["tmux"]="tmux tmux tmux tmux"
    ["jq"]="jq jq jq jq"
)
declare -A PKG_MANAGERS=(
    ["apt"]="apt-get remove --purge -y"
    ["dnf"]="dnf remove -y"
    ["pacman"]="pacman -Rns --noconfirm"
    ["zypper"]="zypper remove -y"
)

# =====================
# Dependency Removal
# =====================
detect_pkg_manager() {
    local managers=("apt" "dnf" "pacman" "zypper")
    for manager in "${managers[@]}"; do
        if command -v "$manager" &>/dev/null; then
            echo "$manager"
            return 0
        fi
    done
    echo "error"
}

remove_dependencies() {
    local pkg_manager="$1"
    local idx

    case $pkg_manager in
        apt) idx=1 ;;
        dnf) idx=2 ;;
        pacman) idx=3 ;;
        zypper) idx=4 ;;
        *)
            echo "❌ Unsupported package manager. Manual removal required:"
            for cmd in "${!DEPENDENCIES[@]}"; do
                echo "  - $cmd"
            done
            exit 1
            ;;
    esac

    for cmd in "${!DEPENDENCIES[@]}"; do
        if command -v "$cmd" &>/dev/null; then
            local pkg_name=$(echo "${DEPENDENCIES[$cmd]}" | cut -d' ' -f$idx)
            echo "🗑️ Removing $cmd ($pkg_name) using $pkg_manager..."
            
            sudo ${PKG_MANAGERS[$pkg_manager]} "$pkg_name" || {
                echo "❌ Failed to remove $pkg_name"
            }
        fi
    done
}

# =====================
# File Cleanup
# =====================
remove_files() {
    echo -e "\n🗑️ Removing installed files from $TARGET_DIR"
    for file in "${FILES[@]}"; do
        if [ -f "$TARGET_DIR/$file" ]; then
            rm -v "$TARGET_DIR/$file"
        fi
    done
}

restore_backup() {
    if [ -d "$BACKUP_DIR" ] && [ "$(ls -A "$BACKUP_DIR")" ]; then
        echo "🔄 Restoring backup files..."
        for backup_file in "$BACKUP_DIR"/*; do
            original_file="${TARGET_DIR}/$(basename "$backup_file" | cut -d'.' -f1)"
            mv -v "$backup_file" "$original_file"
        done
        rmdir "$BACKUP_DIR"
    else
        echo "ℹ️ No backup files found to restore."
    fi
}

cleanup_directory() {
    if [ -d "$TARGET_DIR" ] && [ -z "$(ls -A "$TARGET_DIR")" ]; then
        echo "🧹 Removing empty target directory: $TARGET_DIR"
        rmdir "$TARGET_DIR"
    fi
}

# =====================
# Main Uninstallation
# =====================
echo -e "\n🚀 Starting cli-desk-env uninstallation\n"

# Phase 1: Dependency Removal
pkg_manager=$(detect_pkg_manager)
if [[ $pkg_manager == "error" ]]; then
    echo "❌ No supported package manager found!"
else
    remove_dependencies "$pkg_manager"
fi

# Phase 2: File Cleanup
remove_files
restore_backup
cleanup_directory

# Phase 3: Post-Uninstall
echo -e "\n✅ Uninstallation complete!\n"
