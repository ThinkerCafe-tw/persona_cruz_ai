#!/bin/bash
# This script sets up the git hooks for the project.

HOOKS_DIR="scripts/git_hooks"
GIT_HOOKS_DIR=".git/hooks"

# Ensure the git hooks directory exists
mkdir -p "$GIT_HOOKS_DIR"

# Create a symbolic link to the pre-commit hook
# -f forces the link, overwriting if it exists
# -s makes it a symbolic link
# The path to the hook script must be relative from the .git/hooks directory
ln -sf "../../$HOOKS_DIR/pre-commit" "$GIT_HOOKS_DIR/pre-commit"

# Make the hook executable
chmod +x "$HOOKS_DIR/pre-commit"

echo "✅ Git pre-commit hook set up successfully."
echo "Run 'git commit' to see your AI assistant in action." 