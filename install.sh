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
    ["apt"]="apt-get install -y"
    ["dnf"]="dnf install -y"
    ["pacman"]="pacman -Sy --noconfirm"
    ["zypper"]="zypper install -y"
)

# =====================
# Dependency Management
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

install_dependencies() {
    local pkg_manager="$1"
    local idx
    
    case $pkg_manager in
        apt) idx=1 ;;
        dnf) idx=2 ;;
        pacman) idx=3 ;;
        zypper) idx=4 ;;
        *) 
            echo "❌ Unsupported package manager. Manual installation required:"
            for cmd in "${!DEPENDENCIES[@]}"; do
                echo "  - $cmd"
            done
            exit 1
            ;;
    esac

    for cmd in "${!DEPENDENCIES[@]}"; do
        if ! command -v "$cmd" &>/dev/null; then
            local pkg_name=$(echo "${DEPENDENCIES[$cmd]}" | cut -d' ' -f$idx)
            echo "🔧 Installing $cmd ($pkg_name) using $pkg_manager..."
            
            if [[ $pkg_manager == "pacman" ]]; then
                sudo pacman -Sy --noconfirm "$pkg_name" || {
                    echo "❌ Failed to install $pkg_name"
                    exit 1
                }
            else
                sudo ${PKG_MANAGERS[$pkg_manager]} "$pkg_name" || {
                    echo "❌ Failed to install $pkg_name"
                    exit 1
                }
            fi
        fi
    done
}

# =====================
# File Management
# =====================
verify_files() {
    for file in "${FILES[@]}"; do
        if [ ! -f "$file" ]; then
            echo "❌ Missing required file: $file"
            exit 1
        fi
    done
}

handle_existing_files() {
    local existing=()
    for file in "${FILES[@]}"; do
        [ -e "$TARGET_DIR/$file" ] && existing+=("$file")
    done

    if [ ${#existing[@]} -gt 0 ]; then
        echo "⚠️  Existing files detected:"
        printf "  - %s\n" "${existing[@]}"
        
        PS3="🛠️  Choose handling method: "
        select choice in "Backup-and-Replace" "Force-Replace" "Skip-Existing"; do
            case $choice in
                "Backup-and-Replace")
                    mkdir -p "$BACKUP_DIR"
                    for file in "${existing[@]}"; do
                        backup_file="$BACKUP_DIR/${file}.$(date +%s)"
                        echo "💾 Backing up to $backup_file"
                        mv -v "$TARGET_DIR/$file" "$backup_file"
                    done
                    break
                    ;;
                "Force-Replace")
                    for file in "${existing[@]}"; do
                        rm -v "$TARGET_DIR/$file"
                    done
                    break
                    ;;
                "Skip-Existing")
                    for existing_file in "${existing[@]}"; do
                        FILES=("${FILES[@]/$existing_file}")
                    done
                    FILES=("${FILES[@]}")
                    break
                    ;;
                *) 
                    echo "❌ Invalid option"
                    exit 1
                    ;;
            esac
        done
    fi
}

# =====================
# Main Installation
# =====================
echo -e "\n🚀 Starting cli-desk-env installation\n"

# Phase 1: Dependency Setup
pkg_manager=$(detect_pkg_manager)
if [[ $pkg_manager == "error" ]]; then
    echo "❌ No supported package manager found!"
    exit 1
fi
install_dependencies "$pkg_manager"

# Phase 2: File Verification
verify_files

# Phase 3: Existing File Handling
mkdir -p "$TARGET_DIR"
handle_existing_files

# Phase 4: Installation
echo -e "\n📦 Installing components to $TARGET_DIR"
for file in "${FILES[@]}"; do
    cp -v "$file" "$TARGET_DIR/$file"
    if [[ "$file" == *.sh ]]; then
        chmod +x "$TARGET_DIR/$file"
        echo "  ➕ Made executable: $file"
    fi
done

# Phase 5: Post-install
echo -e "\n✅ Installation complete!"
echo -e "\nNext steps:"
echo "1. Add to tmux.conf: 'source-file $TARGET_DIR/tmux.conf'"
echo "2. Restart tmux sessions"
echo "3. Use F2/F3 to launch the environment\n"
