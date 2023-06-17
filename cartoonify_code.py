import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def cartoonify_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply median blur to reduce noise
    blurred = cv2.medianBlur(gray, 5)

    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Apply bilateral filter for color smoothing
    color = cv2.bilateralFilter(image, 9, 300, 300)

    # Combine color and edges using bitwise and operation
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon


def open_image():
    # Open file dialog to select an image
    file_path = filedialog.askopenfilename(title="Select Image")

    if file_path:
        # Read the image
        image = cv2.imread(file_path)

        # Convert the image to cartoon
        cartoon = cartoonify_image(image)

        # Convert the cartoon image from OpenCV format to PIL format
        cartoon_pil = Image.fromarray(cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB))

        # Resize the cartoon image while maintaining aspect ratio
        width, height = cartoon_pil.size
        max_size = max(width, height)
        if max_size > 800:
            scale_factor = 800 / max_size
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            cartoon_pil = cartoon_pil.resize((new_width, new_height), Image.ANTIALIAS)

        # Display the cartoon image
        cartoon_tk = ImageTk.PhotoImage(cartoon_pil)
        image_label.configure(image=cartoon_tk)
        image_label.image = cartoon_tk


# Create the main application window
window = tk.Tk()
window.title("Image to Cartoon")
window.geometry("800x600")

# Create a button to open the image
open_button = tk.Button(window, text="Open Image", command=open_image)
open_button.pack(pady=10)

# Create a label to display the image
image_label = tk.Label(window)
image_label.pack()

# Run the main event loop
window.mainloop()
