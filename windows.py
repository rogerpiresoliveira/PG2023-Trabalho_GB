from tkinter import Toplevel, Scale, Button, Label
from Editor import ImageEditor
from PIL import Image, ImageTk
from typing import Type
import tkinter as tk
import sticker
import filters
import cv2
import os


def create_image_filter_window(title: str, filter_function, editor: Type[ImageEditor], slider_labels):
    # Cria a janela de diálogo
    dialog = Toplevel(editor.main_window)
    dialog.title(title)

    def update_displayed_image(event=None):
        filtered_image = filter_function(editor.current_image, *get_slider_values())
        editor.display_image(filtered_image)

    def apply_filter(event=None):
        filtered_image = filter_function(editor.current_image, *get_slider_values())
        editor.new_current_image(filtered_image)

    def get_slider_values():
        return [slider.get() for slider, _ in sliders]

    # Cria os sliders e seus rótulos
    sliders = []
    for i, (label, default_value, start, end, resolution) in enumerate(slider_labels):
        label_widget = Label(dialog, text=label)
        slider = Scale(dialog, from_=start, to=end, orient="horizontal", length=300, resolution=resolution, command=update_displayed_image)
        slider.set(default_value if default_value is not None else 0)
        sliders.append((slider, label_widget))
        label_widget.grid(row=i, column=0, sticky='s')
        slider.grid(row=i, column=1)

    # Cria o botão Apply
    apply_button = Button(dialog, text="Apply", command=apply_filter)
    apply_button.grid(row=len(slider_labels), column=0, columnspan=2)

def show_color_overlay_window(editor: Type[ImageEditor]):
    slider_labels = [
        ("Blue", 0, 0, 255, 1),
        ("Green", 0, 0, 255, 1),
        ("Red", 0, 0, 255, 1)
    ]
    create_image_filter_window("Choose Color to Overlay", filters.add_color_overlay, editor, slider_labels)


def show_saturation_window(editor: Type[ImageEditor]):
    slider_labels = [
        ("Factor", 1, 1, 3, 0.01)
    ]
    create_image_filter_window("Choose Saturation Factor", filters.apply_saturation, editor, slider_labels)


def show_binarization_window(editor: Type[ImageEditor]):
    slider_labels = [
        ("Threshold", 122, 0, 255, 1)
    ]
    create_image_filter_window("Choose Threshold to Binarize", filters.binarize, editor, slider_labels)


def show_gaussian_blur_window(editor: Type[ImageEditor]):
    slider_labels = [
        ("Radius", 0, 0, 5, 0.01)
    ]
    create_image_filter_window("Choose Radius to Gaussian Blur", filters.apply_gaussian_blur, editor, slider_labels)


def show_canny_edge_detection_window(editor: Type[ImageEditor]):
    slider_labels = [
        ("Minimum Threshold", 100, 0, 255, 1),
        ("Maximum Threshold", 100, 0, 255, 1)
    ]
    create_image_filter_window("Choose Thresholds for Canny Edge Detection", filters.apply_canny_edge_detection, editor, slider_labels)


def show_sobel_edge_detection_window(editor: Type[ImageEditor]):
    slider_labels = [
        ("Kernel Size", 1, 1, 7, 2)
    ]
    create_image_filter_window("Choose Kernel Size for Sobel Edge Detection", filters.apply_sobel_edge_detection, editor, slider_labels)


def show_dilation_window(editor: Type[ImageEditor]):
    slider_labels = [
        ("Kernel Size", 3, 3, 7, 2),
        ("Iterations", 1, 1, 10, 1)
    ]
    create_image_filter_window("Choose Kernel Size and Iterations for Dilation", filters.apply_dilation, editor, slider_labels)


def show_erosion_window(editor: Type[ImageEditor]):
    slider_labels = [
        ("Kernel Size", 3, 3, 7, 2),
        ("Iterations", 1, 1, 10, 1)
    ]
    create_image_filter_window("Choose Kernel Size and Iterations for Erosion", filters.apply_erosion, editor, slider_labels)

def show_sticker_window(editor: Type[ImageEditor]):
    # Set the folder where the images are located
    images_folder = "fotos\\stickers\\"

    # Get the list of image files in the folder
    image_files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f)) and f.endswith((".png", ".jpg", ".jpeg"))]

    dialog = Toplevel(editor.main_window)
    dialog.title("Stickers")

    # Create a 4x4 grid
    for i in range(4):
        for j in range(4):
            index = i * 4 + j
            if index < len(image_files):
                # Load the image using the PIL library
                image = Image.open(os.path.join(images_folder, image_files[index]))
                # Resize the image while maintaining the aspect ratio
                image.thumbnail((200, 200))

                # Convert the image to the Tkinter format
                image_tk = ImageTk.PhotoImage(image)

                # Create a label to display the image
                label = tk.Label(dialog, image=image_tk)
                label.grid(row=i, column=j)

                # Callback function to open the image when clicked
                def open_image(event, file):
                    sticker.load_images(editor, {'photo': editor.get_current_image(), 'sticker': cv2.imread(f"{images_folder}{file}", cv2.IMREAD_UNCHANGED)})
                    

                # Bind the callback function to the label
                label.bind("<Button-1>", lambda event, file=image_files[index]: open_image(event, file))

                # Keep a reference to the image to prevent it from being garbage collected
                label.image = image_tk