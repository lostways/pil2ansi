import shutil
from dataclasses import dataclass

from PIL import Image

# Get terminal width/height 
TERMINAL_WIDTH = shutil.get_terminal_size().columns
TERMINAL_HEIGHT = shutil.get_terminal_size().lines

#pallets type

@dataclass
class Palettes:
    grayscale =  [ f"\033[0;48;5;{i}m \033[0m" for i in range(232, 256) ],
    grayscale_inverted = [ f"\033[0;48;5;{i}m \033[0m" for i in range(255, 231, -1) ],
    ascii = [' ', '.', ':', '+', '*', '?', '%', '@']
    #color = [ f"\033[0;48;2;{r};{g};{b}m \033[0m" for r in range(0, 256, 16) for g in range(0, 256, 16) for b in range(0, 256, 16) ]
    color = []
 
def convert_img(img_path: str, palette=Palettes.color, width=TERMINAL_WIDTH, alpha=False) -> str:
    """Convert image to ascii art using PIL"""
    img = Image.open(img_path)

    # Resize image and maintain aspect ratio
    new_width = min(width, TERMINAL_WIDTH)
    new_height = int(new_width * img.height / img.width * 0.55)
    img = img.resize((new_width, new_height),resample=Image.NEAREST)
    
    print(f"Image size: {img.width}x{img.height}")

    if palette == Palettes.color:
        img = img.convert('RGBA')
    else:
        # Convert to greyscale
        img = img.convert('LA')

    pixels = img.getdata()
    ascii_str = ''
    if palette == Palettes.color:
        ansi_chars_rgb = []
        for r, g, b, a in pixels:
            if a == 0 and alpha == True:
                ansi_chars_rgb.append(f"\033[0m \033[0m")
            else:
                ansi_chars_rgb.append(f"\033[0;48;2;{r};{g};{b}m \033[0m")

        for i, c in enumerate(ansi_chars_rgb):
            if i % img.width == 0: 
                ascii_str += '\n'
            ascii_str += c
    else:
        chars = palette
        num_chars = len(chars)
        for i,(p,a) in enumerate(pixels):
            idx = int(num_chars * (p / 255))
            idx = min(idx, num_chars - 1)
            if i % img.width == 0: 
                ascii_str += '\n'
            if a == 0 and alpha == True:
                ascii_str += '\033[0m \033[0m'
            else:
                ascii_str += chars[idx]
    return ascii_str
