from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import threading
import windows
import filters
import cv2

class ImageEditor:
    def __init__(self):
        self.stop_camera = False
        self.current_image = None
        self.main_window = tk.Tk()
        self.main_window.state('zoomed')
        self.image_widget = tk.Label(self.main_window)
        self.image_widget.pack()
        self.menu_bar = tk.Menu(self.main_window)
        self.main_window.config(menu=self.menu_bar)
        self.create_menus()

    def create_menus(self):
        # Create the Input menu
        input_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Input", menu=input_menu)
        input_menu.add_command(label="Camera", command=self.open_camera)
        input_menu.add_command(label="Open File", command=self.open_file)
        input_menu.add_command(label="Save Current Image", command=self.save_current_image)
        input_menu.add_command(label="Reset", command=self.reset_file)

        # Create the Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Color Overlay", command=self.color_overlay)
        edit_menu.add_command(label="Add Sticker", command=self.add_sticker)

        # Create the Filters menu
        filters_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Filters", menu=filters_menu)
        filters_menu.add_command(label="Blue Channel Only", command=self.blue_channel_only)
        filters_menu.add_command(label="Green Channel Only", command=self.green_channel_only)
        filters_menu.add_command(label="Red Channel Only", command=self.red_channel_only)
        filters_menu.add_command(label="Invert", command=self.invert_image)
        filters_menu.add_command(label="Grayscale", command=self.grayscale_image)
        filters_menu.add_command(label="Saturation", command=self.saturate_image)
        filters_menu.add_command(label="Binarize", command=self.binarize_image)
        filters_menu.add_command(label="Gaussian Blur", command=self.gaussian_blur)
        filters_menu.add_command(label="Canny Edge Detection", command=self.canny_edge_detection)
        filters_menu.add_command(label="Sobel Edge Detection", command=self.sobel_edge_detection)
        filters_menu.add_command(label="Dilation", command=self.image_dilation)
        filters_menu.add_command(label="Erosion", command=self.image_erosion)
    
    def run(self):
        self.main_window.mainloop()
    
    def display_image(self, opencv_image):
        image_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)))
        self.image_widget.configure(image=image_tk)
        self.image_widget.image = image_tk
    
    def capture_from_camera(self, event):
        if event.char == 'c':
            self.stop_camera = True

    def video_thread(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            self.display_image(frame)
            if self.stop_camera:
                self.current_image = frame
                cap.release()
                cv2.destroyAllWindows()
                break

    def open_camera(self):
        self.stop_camera = False
        thread = threading.Thread(target=self.video_thread)
        thread.daemon = True
        thread.start()
        self.main_window.bind('<KeyPress>', self.capture_from_camera)
    
    def open_file(self):
        file_path = filedialog.askopenfilename()
        self.current_image = cv2.imread(file_path)
        self.display_image(self.current_image)
    
    def new_current_image(self, new_image):
        self.current_image = new_image
    
    def get_current_image(self):
        return self.current_image
    
    def user_decision(self, new_image):
        result = messagebox.askquestion("Question", "Do you want to apply the effect?")

        if result == "yes":
            self.new_current_image(new_image)
        else:
            self.display_image(self.current_image)

    def blue_channel_only(self):
        new_image = filters.only_channel(self.current_image, 0)
        self.display_image(new_image)
        self.user_decision(new_image)

    def green_channel_only(self):
        new_image = filters.only_channel(self.current_image, 1)
        self.display_image(new_image)
        self.user_decision(new_image)

    def red_channel_only(self):
        new_image = filters.only_channel(self.current_image, 2)
        self.display_image(new_image)
        self.user_decision(new_image)

    def invert_image(self):
        new_image = filters.invert(self.current_image)
        self.display_image(new_image)
        self.user_decision(new_image)
    
    def grayscale_image(self):
        new_image = filters.grayscale_average(self.current_image)
        self.display_image(new_image)
        self.user_decision(new_image)

    def color_overlay(self):
        windows.show_color_overlay_window(self)

    def saturate_image(self):
        windows.show_saturation_window(self)
    
    def binarize_image(self):
        windows.show_binarization_window(self)

    def gaussian_blur(self):
        windows.show_gaussian_blur_window(self)

    def canny_edge_detection(self):
        windows.show_canny_edge_detection_window(self)

    def sobel_edge_detection(self):
        windows.show_sobel_edge_detection_window(self)
    
    def image_dilation(self):
        windows.show_dilation_window(self)

    def image_erosion(self):
        windows.show_erosion_window(self)
    
    def add_sticker(self):
        windows.show_sticker_window(self)
    
    def reset_file(self):
        self.display_image(self.current_image)
    
    def save_current_image(self):
        cv2.imwrite("saved_image.jpg", self.current_image)

# Main program
if __name__ == "__main__":
    editor = ImageEditor()
    editor.run()