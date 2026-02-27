# Installation Instructions for orcatools

This guide provides multiple methods to install the orcatools package in a conda environment.

## Method 1: Using pip in a conda environment (Recommended)

### Option A: Install from local directory
```bash
# Create a new conda environment
conda create -n orcatools python=3.10
conda activate orcatools

# Install the package from the project directory
cd /path/to/orcatools
pip install -e .

# Or install without editable mode:
# pip install .
```

### Option B: Install using environment.yml
```bash
# Create conda environment from environment.yml
cd /path/to/orcatools
conda env create -f environment.yml
conda activate orcatools

# Install orcatools in editable mode
pip install -e .
```

## Method 2: Direct installation in existing environment

If you already have a conda environment:
```bash
conda activate your_environment
cd /path/to/orcatools
pip install -e .
```

## Method 3: Development Installation

For development with all optional dependencies:
```bash
conda create -n orcatools-dev python=3.10
conda activate orcatools-dev
cd /path/to/orcatools
pip install -e .[dev]
```

## Verify Installation

After installation, verify that orcatools is installed correctly:
```bash
python -c "import orcatools; print('orcatools successfully installed!')"
```

Or test with a simple example:
```python
from orcatools.inp import ORCAINP
from orcatools.tools import get_input_blocks_from_file
print("Import successful!")
```

## Uninstall

To uninstall orcatools:
```bash
pip uninstall orcatools
```

To remove the conda environment:
```bash
conda deactivate
conda env remove -n orcatools
```

## Notes

- The `-e` flag installs the package in "editable" mode, which means changes to the source code will be immediately reflected without reinstalling.
- The package includes `py3Dmol` for molecular visualization features by default.
- Make sure ORCA software is properly installed and accessible in your system PATH for the tools to work correctly.
