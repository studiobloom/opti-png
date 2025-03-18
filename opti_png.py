import ctypes
import sys
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image

def set_console_title():
    ctypes.windll.kernel32.SetConsoleTitleW("Opti-PNG")

def display_initial_message():
    print("Opti-PNG - Image Optimization Tool")
    print("Opti-PNG will bulk resize, compress and convert non PNG images to an optimized PNG final version.")
    print("Created by John Large aka bloom")
    print("Website: https://studiobloom.xyz")
    print("If this tool helps you, please consider buying me donating:\n$studiobloomxyz on cash app, paypal.me/studiobloomxyz\nBTC @ 33bhGfzcKekYh8oB31Jzv5FYUkdahyC3eA\nETH @ 0xD974b9ab6e897d1128F2aFe98Aa172dE8180D27E")
    print("\n\n")
    print("Choose the directory of the image(s) to be optimized.\nProceed through the following window prompts.")

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    return directory

def get_icon_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'opti_png.ico')
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opti_png.ico')

class DimensionSizeDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Max Dimensions")
        self.iconbitmap(get_icon_path())
        self.geometry("300x300")
        self.resizable(False, False)

        # Initialize with default values
        self.max_width = 2000
        self.max_height = 2000
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Set maximum dimensions of image(s).\nAspect Ratio will remain locked.\n(between 500px-4000px is suggested)")
        label.pack(pady=10)

        width_frame = tk.Frame(self)
        width_frame.pack(pady=5)
        
        width_label = tk.Label(width_frame, text="Maximum Width:")
        width_label.pack(side=tk.LEFT, padx=5)
        
        self.width_entry = tk.Entry(width_frame, width=10)
        self.width_entry.pack(side=tk.LEFT)
        # Set default value
        self.width_entry.insert(0, "2000")
        
        height_frame = tk.Frame(self)
        height_frame.pack(pady=5)
        
        height_label = tk.Label(height_frame, text="Maximum Height:")
        height_label.pack(side=tk.LEFT, padx=5)
        
        self.height_entry = tk.Entry(height_frame, width=10)
        self.height_entry.pack(side=tk.LEFT)
        # Set default value
        self.height_entry.insert(0, "2000")
        
        note_label = tk.Label(self, text="Note: The smaller limit will be applied\nwhile maintaining aspect ratio.")
        note_label.pack(pady=10)

        button = tk.Button(self, text="OK", command=self.set_dimensions)
        button.pack(pady=10)
        
    def set_dimensions(self):
        try:
            width_input = self.width_entry.get().strip()
            height_input = self.height_entry.get().strip()
            
            # Set defaults if empty
            if width_input:
                self.max_width = int(width_input)
            # else max_width remains at default 2000
            
            if height_input:
                self.max_height = int(height_input)
            # else max_height remains at default 2000
            
        except ValueError:
            # Invalid input, keep defaults
            pass
            
        self.destroy()

class DeleteOriginalDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Delete Original Files")
        self.iconbitmap(get_icon_path())
        self.geometry("300x200")
        self.resizable(False, False)

        self.delete_original = False
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Do you want to delete the original image files\nafter they have been converted to PNG?")
        label.pack(pady=10)

        yes_button = tk.Button(self, text="Yes", command=self.set_delete_true)
        yes_button.pack(pady=5)

        no_button = tk.Button(self, text="No", command=self.set_delete_false)
        no_button.pack(pady=5)
        
    def set_delete_true(self):
        self.delete_original = True
        self.destroy()
        
    def set_delete_false(self):
        self.delete_original = False
        self.destroy()

class ProcessSubdirsDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Process Subdirectories")
        self.iconbitmap(get_icon_path())
        self.geometry("400x200")
        self.resizable(False, False)

        self.process_subdirs = False
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Do you want to process images in all subdirectories\nor just the selected directory?")
        label.pack(pady=10)

        subdirs_button = tk.Button(self, text="Include All Subdirectories", command=self.set_process_subdirs_true)
        subdirs_button.pack(pady=5)

        current_dir_button = tk.Button(self, text="Selected Directory Only", command=self.set_process_subdirs_false)
        current_dir_button.pack(pady=5)
        
    def set_process_subdirs_true(self):
        self.process_subdirs = True
        self.destroy()
        
    def set_process_subdirs_false(self):
        self.process_subdirs = False
        self.destroy()

class CustomOutputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Output Directory")
        self.iconbitmap(get_icon_path())
        self.geometry("400x200")
        self.resizable(False, False)

        self.use_custom_output = False
        self.output_directory = None
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Would you like to save all converted PNG images\nto a custom output directory?")
        label.pack(pady=10)

        yes_button = tk.Button(self, text="Yes, use custom output directory", command=self.select_output_dir)
        yes_button.pack(pady=5)

        no_button = tk.Button(self, text="No, save in original locations", command=self.use_original_locations)
        no_button.pack(pady=5)
        
    def select_output_dir(self):
        self.use_custom_output = True
        self.destroy()
        
    def use_original_locations(self):
        self.use_custom_output = False
        self.destroy()

def get_dimensions():
    root = tk.Tk()
    root.withdraw()
    dialog = DimensionSizeDialog(root)
    root.wait_window(dialog)
    return dialog.max_width, dialog.max_height

def get_delete_original_option():
    root = tk.Tk()
    root.withdraw()
    dialog = DeleteOriginalDialog(root)
    root.wait_window(dialog)
    return dialog.delete_original

def get_process_subdirs_option():
    root = tk.Tk()
    root.withdraw()
    dialog = ProcessSubdirsDialog(root)
    root.wait_window(dialog)
    return dialog.process_subdirs

def get_custom_output_option():
    root = tk.Tk()
    root.withdraw()
    dialog = CustomOutputDialog(root)
    root.wait_window(dialog)
    
    if dialog.use_custom_output:
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        return True, output_dir
    else:
        return False, None

def count_images(directory, include_subdirs=False):
    image_count = 0
    
    if include_subdirs:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith((".jpg", ".jpeg", ".gif", ".bmp", ".heic", ".tiff", ".tif", ".webp")):
                    image_count += 1
    else:
        image_count = sum([filename.lower().endswith((".jpg", ".jpeg", ".gif", ".bmp", ".heic", ".tiff", ".tif", ".webp")) 
                          for filename in os.listdir(directory)])
    
    print(f"Optimizable Images found: {image_count}")
    return image_count

def process_image(img_path, max_width, max_height, delete_original=False, custom_output_dir=None, progress_callback=None):
    try:
        filename = os.path.basename(img_path)
        directory = os.path.dirname(img_path)
        
        print(f"Processing image: {filename}")
        
        # Step 1: Loading
        img = Image.open(img_path)
        if progress_callback:
            progress_callback(0.2)  # 20% progress for loading
        
        # Calculate aspect ratio
        width, height = img.size
        aspect_ratio = width / height
        
        # Initialize scaling ratios
        width_ratio = float('inf')
        height_ratio = float('inf')
        
        # Calculate ratios only for enabled dimensions
        if max_width:
            width_ratio = max_width / width
        if max_height:
            height_ratio = max_height / height
        
        # Only resize if we have at least one limit and the image exceeds it
        if (max_width and width > max_width) or (max_height and height > max_height):
            # Use the smaller ratio to ensure both dimensions fit within limits
            ratio = min(width_ratio, height_ratio)
            
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            # Resize the image
            img = img.resize((new_width, new_height), Image.LANCZOS)
            print(f"Resized image from {width}x{height} to {new_width}x{new_height}")
        
        if progress_callback:
            progress_callback(0.6)  # 60% progress after resize

        # Determine where to save the PNG file
        if custom_output_dir:
            output_dir = custom_output_dir
            # Create subdirectory structure if we're processing subdirectories
            if directory.startswith(os.path.commonpath([directory, img_path])):
                rel_path = os.path.relpath(directory, os.path.commonpath([directory, img_path]))
                if rel_path != '.':
                    output_dir = os.path.join(custom_output_dir, rel_path)
                    os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = directory

        # Save as optimized PNG
        png_filename = os.path.splitext(filename)[0] + "_opti.png"
        png_path = os.path.join(output_dir, png_filename)
        img.save(png_path, "PNG", optimize=True)
        print(f"Saved optimized PNG: {png_filename}")
        
        if progress_callback:
            progress_callback(0.8)  # 80% progress after saving
        
        # Delete original file if option is selected
        if delete_original:
            os.remove(img_path)
            print(f"Deleted original image: {filename}")
        
        if progress_callback:
            progress_callback(1.0)  # 100% progress after cleanup
            
        return True
    
    except Exception as e:
        print(f"An error occurred while processing image {filename}: {e}")
        return False

def resize_and_convert(directory, max_width, max_height, delete_original=False, process_subdirs=False, use_custom_output=False, custom_output_dir=None, progress_callback=None):
    image_count = count_images(directory, process_subdirs)
    if image_count == 0:
        print("No optimizable images found.")
        return

    print(f"Processing images in directory: {directory}")
    print(f"Using max width: {max_width}, max height: {max_height}")
    print(f"Processing subdirectories: {'Yes' if process_subdirs else 'No'}")
    
    if use_custom_output and custom_output_dir:
        print(f"Saving all PNG images to: {custom_output_dir}")
        # Create output directory if it doesn't exist
        os.makedirs(custom_output_dir, exist_ok=True)
    
    processed_count = 0
    
    if process_subdirs:
        # Process all subdirectories
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith((".jpg", ".jpeg", ".gif", ".bmp", ".heic", ".tiff", ".tif", ".webp")):
                    img_path = os.path.join(root, filename)
                    if process_image(img_path, max_width, max_height, delete_original, custom_output_dir if use_custom_output else None, progress_callback):
                        processed_count += 1
    else:
        # Process only the selected directory
        for filename in os.listdir(directory):
            if filename.lower().endswith((".jpg", ".jpeg", ".gif", ".bmp", ".heic", ".tiff", ".tif", ".webp")):
                img_path = os.path.join(directory, filename)
                if process_image(img_path, max_width, max_height, delete_original, custom_output_dir if use_custom_output else None, progress_callback):
                    processed_count += 1
    
    print(f"Successfully processed {processed_count} out of {image_count} images.")

if __name__ == "__main__":
    set_console_title()
    display_initial_message()
    directory = select_directory()
    if directory:
        max_width, max_height = get_dimensions()
        process_subdirs = get_process_subdirs_option()
        use_custom_output, custom_output_dir = get_custom_output_option()
        delete_original = get_delete_original_option()
        resize_and_convert(directory, max_width, max_height, delete_original, process_subdirs, use_custom_output, custom_output_dir)
    
    # Keep the command window open and prompt the user to restart
    while True:
        user_input = input("Your conversion is now complete, thank you for using Opti-PNG:)\nType 'r' to run the script again, or press enter to exit:")
        if user_input.lower() == "r":
            set_console_title()
            directory = select_directory()
            if directory:
                max_width, max_height = get_dimensions()
                process_subdirs = get_process_subdirs_option()
                use_custom_output, custom_output_dir = get_custom_output_option()
                delete_original = get_delete_original_option()
                resize_and_convert(directory, max_width, max_height, delete_original, process_subdirs, use_custom_output, custom_output_dir)
        else:
            break