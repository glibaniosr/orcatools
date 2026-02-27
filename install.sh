#!/bin/bash
# Installation script for orcatools in conda environment

set -e  # Exit on error

echo "=========================================="
echo "  orcatools Installation Script"
echo "=========================================="
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH"
    echo "Please install Anaconda or Miniconda first"
    exit 1
fi

# Get environment name from user
read -p "Enter conda environment name (default: orcatools): " ENV_NAME
ENV_NAME=${ENV_NAME:-orcatools}
read -p "Do you want an editable installation? (y/n, default: n): " EDITABLE
EDITABLE=${EDITABLE:-n}

# Check if environment already exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo ""
    read -p "Environment '${ENV_NAME}' already exists. Do you want to use it? (y/n): " USE_EXISTING
    if [[ $USE_EXISTING != "y" && $USE_EXISTING != "Y" ]]; then
        echo "Installation cancelled."
        exit 0
    fi
else
    # Create new environment
    echo ""
    echo "Creating conda environment: ${ENV_NAME}"
    conda create -n "${ENV_NAME}" python=3.10 -y
fi

# Activate environment
echo ""
echo "Activating environment: ${ENV_NAME}"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${ENV_NAME}"

# Install package
echo ""
echo "Installing orcatools (including py3Dmol for visualization)..."
if [[ $EDITABLE == "y" || $EDITABLE == "Y" ]]; then
    pip install -e .[all]
else
    pip install .[all]
fi

# Verify installation
echo ""
echo "Verifying installation..."
if python -c "import orcatools" 2>/dev/null; then
    echo ""
    echo "=========================================="
    echo "  Installation successful!"
    echo "=========================================="
    echo ""
    echo "To use orcatools, activate the environment with:"
    echo "  conda activate ${ENV_NAME}"
    echo ""
    echo "Then you can import it in Python:"
    echo "  from orcatools.inp import ORCAINP"
    echo "  from orcatools.out import ORCAOUT"
    echo ""
else
    echo ""
    echo "Error: Installation verification failed"
    exit 1
fi
