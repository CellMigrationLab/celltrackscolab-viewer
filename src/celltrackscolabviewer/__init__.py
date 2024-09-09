# src/celltrackscolabviewer/__init__.py

__version__ = "0.1.0"

# Importing the widgets for loading and visualizing
from ._widget import load_csv_widget, visualize_widget
from ._sample_data import make_sample_data

# Update __all__ to reflect the correct widgets
__all__ = (
    "load_csv_widget",
    "visualize_widget",
    "make_sample_data",
)

