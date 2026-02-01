# Environment Setup

*Authors: [Jonas](intro.md#jonas), [Julius](intro.md#julius)*

This chapter guides you through setting up your Python environment for energy system modelling.

## Quick Start with Google Colab

You can begin without any local installation using [Google Colab](https://colab.google/). This requires only a Google account.

Navigate to the notebook pages and click the rocket button at the top to open in Colab.

## Local Installation

For local development, we recommend using `conda` to manage your Python environment.

### Installing Conda

1. Download [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Follow the installation instructions for your operating system
3. Open a terminal (or Anaconda Prompt on Windows)

### Creating an Environment

Create a new environment for energy modelling:

```bash
conda create -n energy-modelling python=3.11
conda activate energy-modelling
```

### Installing Required Packages

Install the core packages:

```bash
conda install -c conda-forge numpy pandas matplotlib jupyterlab
```

For energy system modelling, install additional packages:

```bash
conda install -c conda-forge pypsa linopy highspy
```

For geospatial analysis:

```bash
conda install -c conda-forge geopandas cartopy
```

## Running Jupyter Lab

With your environment activated, start Jupyter Lab:

```bash
jupyter lab
```

This opens a browser window with the Jupyter interface.

## Alternative: Using pip

If you prefer pip:

```bash
pip install numpy pandas matplotlib jupyterlab
pip install pypsa linopy highspy
```

:::{warning}
Some geospatial packages (geopandas, cartopy) may require additional system dependencies when using pip.
:::

## VS Code Setup

You can also use [Visual Studio Code](https://code.visualstudio.com/) with the following extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

Select your conda environment as the Python interpreter in VS Code.

## Verifying Installation

Test your installation by running:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("NumPy version:", np.__version__)
print("Pandas version:", pd.__version__)
print("Setup complete!")
```

If no errors appear, you're ready to start modelling!
