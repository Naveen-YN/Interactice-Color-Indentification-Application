# Interactive Color Identification

This Python application provides an interactive interface for identifying colors from images. It allows users to select an image file, detect colors within the image, and copy color codes to the clipboard.

## Installation

1. Install required libraries:

   ```bash
   pip install tkinter ttkthemes pillow numpy scikit-learn matplotlib webcolors
   ```

2. Download the source code:

   ```bash
   git clone https://github.com/Naveen-YN/Interactice-Color-Indentification-Application.git
   ```

3. Navigate to the project directory:

   ```bash
   cd interactive-color-identification
   ```

4. Run the application:

   ```bash
   python Interactive-Color-Detection.py
   ```

## Usage

1. **Select Image**: Click the "Select Image" button to choose an image file from your computer.

2. **Detect Colors**: After selecting an image, click the "Detect Colors" button to analyze the image and display the detected colors.

3. **Copy Color**: Click on any detected color to copy its hexadecimal code to the clipboard.

4. **Pixel Color Detector**: This option opens another window for detecting colors from individual pixels within the image.

## Dependencies

- tkinter: GUI library for Python.
- ttkthemes: Provides themed widget styles for tkinter.
- pillow: Python Imaging Library for image processing.
- numpy: Numerical computing library for array operations.
- scikit-learn: Machine learning library for KMeans clustering.
- matplotlib: Plotting library for visualizing data.
- webcolors: Library for working with color names and codes.
