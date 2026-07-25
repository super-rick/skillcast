#!/bin/bash
# SkillCast Demo Script
# Run this to see the full workflow in your terminal.
# To record as GIF: terminalizer record demo -c terminalizer.yml

set -e
DEMO_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

echo "╔══════════════════════════════════════════════════════╗"
echo "║         SkillCast — Live Demo                        ║"
echo "║  Write Skills once, deliver everywhere.              ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Step 1: Install
echo "━━━ Step 1: Install ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "\$ pip install skillcast"
pip install -q skillcast
echo "✅ Installed: $(skillcast --version 2>/dev/null || python -c 'import skillcast; print(skillcast.__version__)')"
echo ""

# Step 2: List formats
echo "━━━ Step 2: See what's supported ━━━━━━━━━━━━━━━━━━━━━"
echo "\$ skillcast list"
skillcast list
echo ""

# Step 3: Create a skill
echo "━━━ Step 3: Create a Skill template ━━━━━━━━━━━━━━━━━━"
echo "\$ skillcast init java-interview"
skillcast init java-interview
echo ""
echo "\$ cat java-interview.yaml"
cat java-interview.yaml
echo ""

# Step 4: Convert to all platforms
echo "━━━ Step 4: Convert to ALL platforms ━━━━━━━━━━━━━━━━━"
echo "\$ skillcast convert java-interview.yaml --all -o output"
skillcast convert java-interview.yaml --all -o output
echo ""

# Step 5: Show output
echo "━━━ Step 5: Output files ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "\$ ls -1 output/"
ls -1 output/
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉  Done! 4 platform formats from 1 Skill definition."
echo ""

# Cleanup
cd "$DEMO_DIR"
rm -rf "$TMP_DIR"
