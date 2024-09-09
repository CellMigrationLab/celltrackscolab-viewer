from magicgui import magic_factory
import napari
import pandas as pd
import pathlib
import os
import numpy as np
import gzip
from skimage import io
from napari.utils.notifications import show_info, show_warning, show_error
from tifffile import TiffFile  # For reading metadata from TIFF files

# Global variables to store the loaded dataframe, filenames, and the folder containing TIFF files
loaded_df = None
raw_filenames = []
visualize_widget_instance = None  # Store the widget instance here
tiff_folder = None  # Path to the folder containing TIFF files

# Helper to detect gzip files
def is_gzip(file_path):
    """Helper function to detect if the file is gzip compressed."""
    with open(file_path, 'rb') as f:
        return f.read(2) == b'\x1f\x8b'  # Magic number for gzip files

# Function to load the CSV file
def load_csv_file(csv_file):
    """Simple function to load CSV (gzipped or not)."""
    if not csv_file:
        return None
    
    try:
        if is_gzip(csv_file):
            with gzip.open(csv_file, 'rt') as f:
                df = pd.read_csv(f)
        else:
            df = pd.read_csv(csv_file)
        print(f"Loaded CSV with {len(df)} rows.")  # Debug message
        return df
    except Exception as e:
        show_error(f"Error loading CSV: {e}")
        return None

# Function to recursively search for TIFF files in a folder
def find_tiff_files(folder, file_name):
    """Recursively search for a TIFF file matching the given file_name in a folder."""
    for root, _, files in os.walk(folder):
        for ext in ['.tif', '.tiff']:
            tiff_file_path = os.path.join(root, f"{file_name}{ext}")
            if os.path.exists(tiff_file_path):
                return tiff_file_path
    return None

# Function to load pixel calibration (resolution/scale) from TIFF metadata
def load_pixel_calibration(tiff_file):
    """Load pixel calibration (resolution/scale) from TIFF metadata, if available."""
    try:
        with TiffFile(tiff_file) as tif:
            if tif.pages[0].tags.get("XResolution") and tif.pages[0].tags.get("YResolution"):
                x_res = tif.pages[0].tags["XResolution"].value
                y_res = tif.pages[0].tags["YResolution"].value
                scale_x = x_res[1] / x_res[0]
                scale_y = y_res[1] / y_res[0]
                return (scale_y, scale_x)  # Return Y first, since Napari expects (scale_y, scale_x)
    except Exception as e:
        show_error(f"Error reading pixel calibration from TIFF metadata: {e}")
    return None

# Function to load the corresponding TIFF file
def load_tiff_file(file_name):
    """Load a TIFF file corresponding to the given file_name."""
    if not tiff_folder or not os.path.isdir(tiff_folder):
        show_warning("No valid TIFF folder specified.")
        return None, None  # Ensure a tuple is always returned

    tiff_file = find_tiff_files(tiff_folder, file_name)

    if tiff_file:
        try:
            image = io.imread(tiff_file)
            scale = load_pixel_calibration(tiff_file)  # Load pixel calibration from metadata
            return image, scale
        except Exception as e:
            show_error(f"Error loading TIFF file {tiff_file}: {e}")
            return None, None  # Ensure a tuple is always returned in case of an error
    else:
        show_warning(f"No TIFF file found for {file_name}.")
        return None, None  # Ensure a tuple is always returned when no file is found

# Function to visualize tracks and load TIFF files
def visualize_tracks(df, file_name):
    """Visualize tracks and the corresponding TIFF file based on the selected file name."""
    viewer = napari.current_viewer()

    # Filter the DataFrame by the selected file name
    if file_name is None:
        show_warning("No file name selected for visualization.")
        return

    if 'File_name_raw' in df.columns:
        filtered_df = df[df['File_name_raw'] == file_name]
    elif 'File_name' in df.columns:
        filtered_df = df[df['File_name'] == file_name]
    else:
        show_error("No valid file name column found in the CSV.")
        return

    # Ensure the required columns are present
    required_columns = ['TRACK_ID', 'POSITION_X', 'POSITION_Y', 'POSITION_Z', 'POSITION_T']
    if not all(col in filtered_df.columns for col in required_columns):
        show_error("CSV is missing required columns for track visualization.")
        return

    # Reformat the track data to match Napari's expected format: [track_id, t, y, x, z]
    track_ids = filtered_df['TRACK_ID'].unique()
    track_data = []

    for track_id in track_ids:
        track_points = filtered_df[filtered_df['TRACK_ID'] == track_id]
        for _, row in track_points.iterrows():
            track_data.append([
                track_id,  # Track ID
                row['POSITION_T'],  # Time (t)
                row['POSITION_Z'],   # Z position
                row['POSITION_Y'],  # Y position
                row['POSITION_X']  # X position
            ])

    track_data = np.array(track_data)

    # Add the tracks to the viewer and ensure they are above the microscopy image
    try:
        viewer.add_tracks(track_data, name=f"Tracks - {file_name}", opacity=1.0)
        show_info(f"Displayed {len(track_ids)} tracks for {file_name}.")
    except ValueError as e:
        show_error(f"Error displaying tracks: {e}")
        print(f"Error displaying tracks: {e}")

    # Load and display the corresponding TIFF file
    image, scale = load_tiff_file(file_name)
    if image is not None:
        viewer.add_image(image, name=f"Image - {file_name}", blending="additive", opacity=0.6, scale=scale)

    # Preserve the dropdown choices after visualization
    visualize_widget_instance.file_name.choices = [None] + raw_filenames  # Reload choices

# Widget to load CSV and TIFF folder
@magic_factory(call_button="Load Data", tiff_folder_path={"mode": "d"})
def load_csv_widget(csv_file: pathlib.Path = None, tiff_folder_path: pathlib.Path = None):
    """Widget to load the CSV file and optionally a folder containing TIFF files."""
    global loaded_df, raw_filenames, visualize_widget_instance, tiff_folder
    viewer = napari.current_viewer()

    # Load the CSV file
    df = load_csv_file(csv_file)
    if df is None:
        show_error("Failed to load CSV.")
        return

    # Store the loaded dataframe in the global variable
    loaded_df = df

    # Update the TIFF folder path
    tiff_folder = str(tiff_folder_path) if tiff_folder_path else None

    # Update the file_name choices based on CSV content
    if 'File_name_raw' in df.columns:
        raw_filenames = df['File_name_raw'].unique().tolist()
    elif 'File_name' in df.columns:
        raw_filenames = df['File_name'].unique().tolist()
    else:
        show_error("No valid file name column found in the CSV.")
        return

    # Create the visualize widget and dock it (only if it's not already docked)
    if visualize_widget_instance is None:
        visualize_widget_instance = visualize_widget()
        viewer.window.add_dock_widget(visualize_widget_instance, name="Visualize Tracks")

    # Update the file_name choices dynamically, and preserve options after visualization
    visualize_widget_instance.file_name.choices = [None] + raw_filenames  # Ensure the dropdown is updated

    # Display a message about the number of rows and file names loaded
    show_info(f"CSV loaded with {len(df)} rows and {len(raw_filenames)} file names.")
    print(f"CSV loaded with {len(df)} rows and {len(raw_filenames)} file names.")  # Debug message

    # Attach a listener to layer removal to preserve file_name choices
    def on_layer_removed(event):
        visualize_widget_instance.file_name.choices = [None] + raw_filenames  # Reload choices if layers are removed

    viewer.layers.events.removed.connect(on_layer_removed)  # Listen for layer removal

# Widget to visualize selected file's tracks and corresponding TIFF file
@magic_factory(call_button="Visualize Tracks", file_name={"widget_type": "ComboBox", "choices": []})
def visualize_widget(file_name: str = None):
    """Widget to visualize tracks and corresponding TIFF file based on the selected file name."""
    global loaded_df, raw_filenames
    viewer = napari.current_viewer()

    # If no CSV has been loaded, show an error
    if loaded_df is None or not raw_filenames:
        show_warning("No CSV loaded. Please load a CSV first.")
        return

    # Visualize the selected file's tracks
    visualize_tracks(loaded_df, file_name)

