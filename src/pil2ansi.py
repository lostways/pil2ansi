import shutil
from dataclasses import dataclass
from typing import Protocol, Tuple, Literal
from PIL import Image

# Get terminal width/height
TERMINAL_WIDTH = shutil.get_terminal_size().columns
TERMINAL_HEIGHT = shutil.get_terminal_size().lines

# PIL color modes
PIL_COLOR = Literal["RGBA", "LA"]


# Palettes for converting pixels to characters
class Palette(Protocol):
    def pixel_to_char(self, pixel: Tuple, alpha: bool) -> str:
        ...

    @property
    def pil_color(self) -> PIL_COLOR:
        ...


@dataclass
class PaletteColor:
    pil_color: PIL_COLOR = "RGBA"

    def pixel_to_char(
        self, pixel: Tuple[int, int, int, int], alpha=False
    ) -> str:
        r, g, b, a = pixel

        if a == 0 and alpha == True:
            return f"\033[0m \033[0m"

        return f"\033[0;48;2;{r};{g};{b}m \033[0m"


@dataclass
class PaletteGrayscale:
    invert: bool = False
    pil_color: PIL_COLOR = "LA"

    def pixel_to_char(self, pixel: Tuple[int, int], alpha=False) -> str:
        p, a = pixel

        if a == 0 and alpha == True:
            return f"\033[0m \033[0m"

        num_values = 23

        if self.invert == True:
            val = 255 - int(p * num_values / 255)
        else:
            val = 232 + int(p * num_values / 255)

        print(f"p: {p}, val: {val}")
        return f"\033[0;48;5;{val}m \033[0m"


@dataclass
class PaletteAscii:
    pil_color: PIL_COLOR = "LA"
    ascii_palette = [".", ",", ":", "+", "*", "?", "%", "@"]

    def pixel_to_char(self, pixel: Tuple[int, int], alpha=False) -> str:
        p, a = pixel

        if a == 0 and alpha == True:
            return f"\033[0m \033[0m"

        num_values = len(self.ascii_palette)  # 8

        val = round(p * num_values / 255) - 1

        # print(f'p: {p}, val_pre: {val_pre}, val: {val}')
        return self.ascii_palette[val]


@dataclass
class Palettes:
    color = PaletteColor()
    grayscale = PaletteGrayscale()
    grayscale_inverted = PaletteGrayscale(invert=True)
    ascii = PaletteAscii()


def convert_img(
    img: Image.Image,
    palette: Palette = Palettes.color,
    width: int = -1,
    alpha=False,
) -> str:
    """Convert image to ascii art using PIL"""

    # Resize image and maintain aspect ratio
    new_width: int = 0
    new_height: int = 0

    if width < 0:
        new_width = img.width
        new_height = img.height
    else:
        new_width = width
        new_height = round(new_width * (img.height / img.width))
        img = img.resize((new_width, new_height), resample=Image.NEAREST)

    # crop image to terminal width
    if new_width > TERMINAL_WIDTH:
        img = img.crop((0, 0, TERMINAL_WIDTH, new_height))

    print(f"Image size: {img.width}x{img.height}")

    img = img.convert(palette.pil_color)

    pixels = img.getdata()
    ascii_str = ""
    for i, p in enumerate(pixels):
        if i % img.width == 0:
            ascii_str += "\n"
        else:
            ascii_str += palette.pixel_to_char(p, alpha)
    return ascii_str
