# celltrackscolab-viewer

[![License MIT](https://img.shields.io/pypi/l/celltrackscolab-viewer.svg?color=green)](https://github.com/CellMigrationLab/celltrackscolab-viewer/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/celltrackscolab-viewer.svg?color=green)](https://pypi.org/project/celltrackscolab-viewer)
[![Python Version](https://img.shields.io/pypi/pyversions/celltrackscolab-viewer.svg?color=green)](https://python.org)
[![tests](https://github.com/CellMigrationLab/celltrackscolab-viewer/workflows/tests/badge.svg)](https://github.com/CellMigrationLab/celltrackscolab-viewer/actions)
[![codecov](https://codecov.io/gh/CellMigrationLab/celltrackscolab-viewer/branch/main/graph/badge.svg)](https://codecov.io/gh/CellMigrationLab/celltrackscolab-viewer)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/celltrackscolab-viewer)](https://napari-hub.org/plugins/celltrackscolab-viewer)

A simple plugin to visualize tracks stored in the CellTracksColab format

----------------------------------

# CellTracksColab Viewer: Alpha Testing

Thank you for participating in the alpha testing of the **CellTracksColab Viewer** plugin! Please follow the steps below to install and test the plugin in Napari.

## Prerequisites

Before installing the plugin, make sure you have the following set up:

1. **Python 3.7 or later**: You can download it from the official [Python website](https://www.python.org/).
2. **Napari**: If you don’t already have Napari installed, you can install it via `pip` or use Conda to manage your environment.

   To install Napari with `pip`:

   ```bash
   pip install "napari[all]"
   ```

   Alternatively, you can install it using Conda (recommended for managing Python environments):

   ```bash
   conda create -n napari-env python=3.9
   conda activate napari-env
   pip install napari
   ```

## Step 1: Clone the Plugin Repository

1. Open a terminal or command prompt.
2. Clone the plugin repository from GitHub:

   ```bash
   git clone https://github.com/CellMigrationLab/celltrackscolab-viewer.git
   cd celltrackscolab-viewer
   ```

This will create a local copy of the plugin repository on your computer.

## Step 2: Install the Plugin Locally

1. After cloning the repository, navigate to the plugin folder (if not already there).
2. Install the plugin in editable mode:

   ```bash
   pip install -e .
   ```

   The `-e` flag installs the plugin in "editable" mode, allowing you to make changes and test them immediately without needing to reinstall the plugin.

## Step 3: Run Napari and Test the Plugin

1. Once the plugin is installed, you can start Napari by typing:

   ```bash
   napari
   ```

2. In Napari, go to the **Plugins** menu and look for **CellTracksColab Viewer**. From here, you can:
   - **Load CSV data**: Use the plugin to load track data from CSV files. Here you should open the **merged_Spots.csv** file
   - **Load TIFF images (optional)**: You can load corresponding microscopy TIFF images and overlay them with track data.
   - **Visualize Tracks**: Select filenames and visualize the tracks in the Napari viewer.

3. test data is available [here](https://zenodo.org/records/11286110)


## Step 4: Reporting Bugs and Providing Feedback

If you encounter any issues or have feedback, please report them by creating an issue in the GitHub repository:

1. Go to the [Issues section](https://github.com/CellMigrationLab/celltrackscolab-viewer/issues) of the repository.
2. Create a new issue, providing as much detail as possible, including:
   - Steps to reproduce the issue.
   - Screenshots or error messages (if applicable).
   - Napari version and operating system (Windows, macOS, or Linux).

Thank you for your time and feedback!


## Step 5: Installation  instructions when ready


This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/stable/plugins/index.html
-->

## Installation

You can install `celltrackscolab-viewer` via [pip]:

    pip install celltrackscolab-viewer



To install latest development version :

    pip install git+https://github.com/CellMigrationLab/celltrackscolab-viewer.git


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT] license,
"celltrackscolab-viewer" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/CellMigrationLab/celltrackscolab-viewer/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
