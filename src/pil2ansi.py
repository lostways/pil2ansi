import shutil
from dataclasses import dataclass
from typing import Protocol, Tuple, Literal
from PIL import Image

# Get terminal width/height 
TERMINAL_WIDTH = shutil.get_terminal_size().columns
TERMINAL_HEIGHT = shutil.get_terminal_size().lines

#pallets type

PIL_COLOR = Literal['RGBA', 'LA']

class Palette(Protocol):
    def pixel_to_char(self, pixel: Tuple, alpha: bool) -> str:
        ...

    @property
    def pil_color(self) -> PIL_COLOR:
        ...

@dataclass
class PaletteColor():
    pil_color: PIL_COLOR = 'RGBA'
    def pixel_to_char(self, pixel: Tuple[int,int,int,int], alpha=False) -> str:
        r,g,b,a = pixel

        if a == 0 and alpha == True:
            return f"\033[0m \033[0m"

        return f"\033[0;48;2;{r};{g};{b}m \033[0m"

@dataclass
class PaletteGrayscale():
    pil_color: PIL_COLOR = 'LA'
    def pixel_to_char(self, pixel: Tuple[int,int], alpha=False) -> str:
        p,a = pixel

        if a == 0 and alpha == True:
            return f"\033[0m \033[0m"

        num_values = 24
        val = 255 - int(p * num_values / 255)
        return f"\033[0;48;5;{val}m \033[0m"

@dataclass
class PaletteGrayscaleInverted():
    pil_color: PIL_COLOR = 'LA'
    def pixel_to_char(self, pixel: Tuple[int,int], alpha=False) -> str:
        p,a = pixel

        if a == 0 and alpha == True:
            return f"\033[0m \033[0m"

        num_values = 24
        val = 232 + (255 - (255 - int(p * num_values / 255)))
        return f"\033[0;48;5;{val}m \033[0m"

@dataclass
class PaletteAscii():
    pil_color: PIL_COLOR = 'LA'
    ascii_palette = [' ', '.', ':', '+', '*', '?', '%', '@']
    def pixel_to_char(self, pixel: Tuple[int,int], alpha=False) -> str:
        p,a = pixel

        if a == 0 and alpha == True:
            return f"\033[0m \033[0m"

        num_values = len(self.ascii_palette)
        val = int(p * num_values / 255)
        return self.ascii_palette[val]

@dataclass
class Palettes:
    color = PaletteColor()
    grayscale =  PaletteGrayscale()
    grayscale_inverted = PaletteGrayscaleInverted()
    ascii = PaletteAscii()

def convert_img(img: Image.Image, palette: Palette = Palettes.color, width=TERMINAL_WIDTH, alpha=False) -> str:
    """Convert image to ascii art using PIL"""

    # Resize image and maintain aspect ratio
    new_width = min(width, img.width)
    new_height = int(new_width * img.height / img.width * 0.55)
    img = img.resize((new_width, new_height),resample=Image.NEAREST)
    
    print(f"Image size: {img.width}x{img.height}")

    img = img.convert(palette.pil_color)

    pixels = img.getdata()
    ascii_str = ''
    for i,p in enumerate(pixels):
        if i % img.width == 0: 
            ascii_str += '\n'
        else:
            ascii_str += palette.pixel_to_char(p, alpha)
    return ascii_str
