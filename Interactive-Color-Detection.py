import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import webcolors
import customtkinter
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
import subprocess


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Interactive Color Identification")
        self.file_path = None
        self.img_array = None
        
        # Create a canvas widget for displaying the selected image
        self.canvas = tk.Canvas(self.master, width=1080, height=750, highlightthickness=0, bd=0, relief='solid', bg='#2b2b2b')
        self.canvas.grid(row=0, column=0, rowspan=10, padx=20, pady=20, sticky='nsew')
       
        # Create side panel
        self.side_panel = tk.Frame(self.master, height=1000, width=self.master.winfo_screenwidth() * 0.2, bg='#2b2b2b')
        self.side_panel.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

        # Configure the columns to have equal weight and expand to fill extra space
        self.side_panel.columnconfigure(0, weight=1)
        self.side_panel.columnconfigure(1, weight=1)

        # Create a label widget for the title
        self.title_label = customtkinter.CTkLabel(self.side_panel, text='Color Detector', font=('Helvetica', 28))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky='nsew')

        # Create a button widget for selecting image file
        self.select_button = customtkinter.CTkButton(self.side_panel, text='Select Image', command=self.open_file)
        self.select_button.grid(row=1, column=0, padx=30, pady=0, sticky='w')

        # Create a button widget for detecting colors
        self.detect_button = customtkinter.CTkButton(self.side_panel, text='Detect Colors', command=self.detect_colors)
        self.detect_button.grid(row=1, column=0, padx=30, pady=0, sticky='e')

        # Create a button widget for pixel color detection
        self.pixel_detector_button = customtkinter.CTkButton(self.side_panel, text='Pixel Color Detector', command=self.pixel_color_detector)
        self.pixel_detector_button.grid(row=2, column=0, padx=100, pady=10, sticky='we')


        # Create a label widget for displaying the detected colors
        self.colors_label = customtkinter.CTkLabel(self.side_panel, text='Detected Colors:',font=('Helvetica', 14))
        self.colors_label.grid(row=3, column=0, columnspan=2, padx=10, pady=8, sticky='nsew')

        # Create a canvas widget for displaying the detected colors
        self.colors_canvas = tk.Canvas(self.side_panel, width=350, height=470, highlightthickness=0, bd=0, relief='solid', bg='#2b2b2b')
        self.colors_canvas.grid(row=6, column=0, padx=10, pady=20, sticky='w')

        # Displays copy to clipboard
        self.copy_message = customtkinter.CTkLabel(self.side_panel, text="", font=("Helvetica", 20))
        self.copy_message.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")

    #It is used for to open another window of the Pixel Color Detection
    def pixel_color_detector(self):
        # Replace `path/to/python/file.py` with the path to your Python file
        subprocess.Popen(['python', 'Pixel Color Detector.py'])

    #File Uploader
    def open_file(self):
        # Open file dialog to select image file
        self.file_path = filedialog.askopenfilename()
        # If a file is selected, display it on canvas and enable the detect button
        if self.file_path:
            img = Image.open(self.file_path)
            max_size = (self.canvas.winfo_width(), self.canvas.winfo_height())
            img.thumbnail(max_size, Image.LANCZOS)
            self.img_array = np.array(img)
            self.img = Image.fromarray(self.img_array)
            self.tk_img = ImageTk.PhotoImage(self.img)
            canvas_center_x = self.canvas.winfo_width() // 2
            canvas_center_y = self.canvas.winfo_height() // 2
            self.canvas.create_image(canvas_center_x, canvas_center_y, anchor="center", image=self.tk_img)
            self.detect_button.configure(state="normal")

    #Color Identifier
    def detect_colors(self):
        # Flatten the image array
        img_array = self.img_array.reshape((-1, 3))

        # Run KMeans clustering algorithm to detect colors
        kmeans = KMeans(n_clusters=25, random_state=0, n_init=10).fit(img_array)
        colors = kmeans.cluster_centers_.astype(int)

        # Convert the detected colors to hex codes and color names
        color_info = []
        for color in colors:
            hex_code = '#%02x%02x%02x' % tuple(color)
            try:
                color_name = webcolors.hex_to_name(hex_code)
            except ValueError:
                color_name = ""
            color_info.append((hex_code, color_name))

        # Display the detected colors on canvas
        self.colors_canvas.delete("all")
        x, y = 0, 0
        for i, color in enumerate(color_info):
            hex_code = color[0]
            color_name = color[1]
            # Create the color box canvas
            color_box = tk.Canvas(self.colors_canvas, width=70, height=50, bd=0, highlightthickness=0)
            color_box.place(x=x, y=y)
            # Add a rectangle to the color box canvas
            color_box.create_rectangle(0, 0, 70, 50, fill=hex_code, outline="")
            # Bind the copy color function to the color box canvas
            color_box.bind("<Button-1>", lambda event, color=hex_code: self.copy_color(color))
            # Add the color name and hex code label to the canvas
            if color_name:
                text = f"{color_name}\n{hex_code}"
            else:
                text = hex_code
            color_text = tk.Label(self.colors_canvas, text=text, font=("Helvetica", 10), bg="white", fg="black")
            color_text.place(x=x+10, y=y+60, anchor="w")  # adjust y-coordinate to 60
            # Add a space between each pallet
            if (i+1) % 5 == 0:
                x, y = 0, y + 100
            else:
                x += 70
        # Configure the scroll region of the canvas
        self.colors_canvas.config(scrollregion=self.colors_canvas.bbox("all"))

    #Color Code copier
    def copy_color(self, color):
    # Copy the color code to clipboard
        self.master.clipboard_clear()
        self.master.clipboard_append(color)
        message = f"Color {color} copied to clipboard!"
        self.copy_message.configure(text=message)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

root = tk.Tk()
# Load background image
bg_image = tk.PhotoImage(file="bg2.png")
# Get window size
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
# Resize image to fit window size
resized_image = bg_image.zoom(int(bg_image.width() / window_width),int(bg_image.height() / window_height))
# Create a label with the background image
bg_label = tk.Label(root, image=resized_image)
# Place the label at the top-left corner
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
#Application alternate title
root.title("Interactive Color Identification")
#Application Icon
root.iconbitmap("color.ico")
# Maximize the window
root.state('zoomed')
app = App(root)
root.mainloop()
