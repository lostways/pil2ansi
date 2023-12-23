from PIL import Image
import shutil

# Get terminal width/height 
TERMINAL_WIDTH = shutil.get_terminal_size().columns
TERMINAL_HEIGHT = shutil.get_terminal_size().lines

"""
print(f"Detected terminal width: {width}")
print(f"Detected terminal height: {height}")

exit()
"""

def convert_img(img_path: str) -> str:
    """Convert image to ascii art using PIL"""
    img = Image.open(img_path)

    # Resize image and maintain aspect ratio
    new_width = TERMINAL_WIDTH
    new_height = img.height
    img.thumbnail((new_width, new_height))
    print(f"Image size: {img.width}x{img.height}")

    # Convert to greyscale
    img = img.convert('L')

    # Map pixels to ascii characters
    chars = [' ', '.', ':', '+', '*', '?', '%', '@']  
    num_chars = len(chars)

    pixels = img.getdata()
    pixel_to_idx = []
    for p in pixels:
        idx = int(num_chars * (p / 255))
        idx = min(idx, num_chars - 1)
        pixel_to_idx.append(idx)

    ascii_str = ''
    for i in range(len(pixel_to_idx)):
        if i % img.width == 0:
            ascii_str += '\n'
        ascii_str += chars[pixel_to_idx[i]]
    
    return ascii_str
