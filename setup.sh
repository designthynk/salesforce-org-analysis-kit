#!/bin/bash

# Salesforce Org Analysis - Project Setup Script
# Usage: ./setup.sh [ORG_ALIAS]

if [ -z "$1" ]; then
    echo "Usage: ./setup.sh [ORG_ALIAS]"
    echo "Example: ./setup.sh my-org-prod"
    exit 1
fi

ORG_ALIAS=$1
BASE_DIR=$(pwd)
FORCE_APP_DIR="$BASE_DIR/force-app/$ORG_ALIAS"
DATA_DIR="$BASE_DIR/scripts/data/$ORG_ALIAS"
SCRIPTS_DIR="$BASE_DIR/scripts"

echo "=========================================="
echo "Setting up analysis project for: $ORG_ALIAS"
echo "=========================================="

# 1. Create Directory Structure
echo "Creating directories..."
mkdir -p "$FORCE_APP_DIR"
mkdir -p "$DATA_DIR"
mkdir -p "outputs"

# 2. Install Dependencies
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found."
fi

# 3. Copy Templates
echo "Copying script templates..."
mkdir -p "$SCRIPTS_DIR"

# Copy extract_metadata.py (generic helper)
cp "templates/extract_metadata.py" "$SCRIPTS_DIR/"

# Copy export_data.py as a starting point for the custom script
# We rename it to encourage customization
TARGET_SCRIPT="$SCRIPTS_DIR/export_$ORG_ALIAS.py"
cp "templates/export_data.py" "$TARGET_SCRIPT"

echo "Created script draft: $TARGET_SCRIPT"

# 4. Success Message
echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo "Next Steps:"
echo "1. Retrieve Metadata:"
echo "   sf project retrieve start --manifest templates/package.xml --target-org $ORG_ALIAS --output-dir $FORCE_APP_DIR"
echo ""
echo "2. Customize Export Script:"
echo "   Edit $TARGET_SCRIPT"
echo "   - Update TARGET_ORG_ALIAS to '$ORG_ALIAS'"
echo "   - Update TIER_1_OBJECTS and TIER_2_OBJECTS queries with valid fields"
echo ""
echo "3. Run Analysis:"
echo "   Follow the steps in README.md"
