import shutil
from dataclasses import dataclass
from typing import Protocol, Tuple, Literal, LiteralString, Union
from PIL import Image

# Get terminal width/height
TERMINAL_WIDTH = shutil.get_terminal_size().columns
TERMINAL_HEIGHT = shutil.get_terminal_size().lines

# PIL color modes
PIL_COLOR = Literal["RGBA", "LA"]
PIXEL = Tuple[int, ...]
PIXEL_RGBA = Tuple[int, int, int, int]
PIXEL_LA = Tuple[int, int]


# Palettes for converting pixels to characters
class Palette(Protocol):
    def pixel_to_color(self, pixel_fg: Tuple, pixel_bg: Tuple) -> str:
        ...

    @property
    def pil_color(self) -> PIL_COLOR:
        ...


@dataclass
class PaletteColor:
    pil_color: PIL_COLOR = "RGBA"

    def pixel_to_color(self, pixel_fg: PIXEL_RGBA, pixel_bg: PIXEL_RGBA) -> str:
        r, g, b, a = pixel_fg
        r2, g2, b2, a2 = pixel_bg

        format1 = 1 if a == 0 else 2  # 2 is RGB, 1 is transparent
        format2 = 1 if a2 == 0 else 2  # 2 is RGB, 1 is transparent

        return f"\033[38;{format1};{r};{g};{b};48;{format2};{r2};{g2};{b2}m"


@dataclass
class PaletteGrayscale:
    invert: bool = False
    pil_color: PIL_COLOR = "LA"

    def pixel_to_color(self, pixel_fg: PIXEL_LA, pixel_bg: PIXEL_LA) -> str:
        p1, a1 = pixel_fg
        p2, a2 = pixel_bg

        format1 = 1 if a1 == 0 else 5  # 5 is 8-bit, 1 is transparent
        format2 = 1 if a2 == 0 else 5  # 5 is 8-bit, 1 is transparent

        num_values = 23

        if self.invert == True:
            val_fg = 255 - int(p1 * num_values / 255)
            val_bg = 255 - int(p2 * num_values / 255)
        else:
            val_fg = 232 + int(p1 * num_values / 255)
            val_bg = 232 + int(p2 * num_values / 255)

        return f"\033[38;{format1};{val_fg};48;{format2};{val_bg}m"


@dataclass
class PaletteAscii:
    pil_color: PIL_COLOR = "LA"
    palette_chars = [".", ",", ":", "+", "*", "?", "%", "@"]

    def pixel_to_color(self, pixel_fg: PIXEL_LA, pixel_bg: PIXEL_LA) -> str:
        p1, a1 = pixel_fg
        p2, _ = pixel_bg

        p = p1 if a1 != 0 else p2

        num_values = len(self.palette_chars) - 1
        val = round(p * num_values / 255)

        return self.palette_chars[val]


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
    alpha=True,
) -> str:
    """Convert image to ascii art using PIL"""

    # Convert image to palette color mode
    img = img.convert(palette.pil_color)

    # Resize image and maintain aspect ratio
    new_width: int = 0
    new_height: int = 0

    if width < 0:
        new_width = img.width
    else:
        new_width = width

    new_height = round(new_width * (img.height / img.width))
    img = img.resize((new_width, new_height), resample=Image.NEAREST)

    # crop image to terminal width
    if new_width > TERMINAL_WIDTH:
        img = img.crop((0, 0, TERMINAL_WIDTH, new_height))

    pixels = img.getdata()

    reset_char: LiteralString = "\033[0m"
    transparent_char: LiteralString = f" "
    unicode_upper_char: LiteralString = "\u2580"
    unicode_lower_char: LiteralString = "\u2584"

    ascii_str: str = ""
    for i in range(len(pixels) // img.width):
        for j in range(img.width):
            if i % 2 == 0:
                pixel_fg: PIXEL
                pixel_bg: PIXEL

                pixel_fg = pixels[i * img.width + j]
                if i < img.height - 1:
                    pixel_bg = pixels[(i + 1) * img.width + j]
                else:
                    pixel_bg = tuple(
                        [255 for _ in pixel_fg[:-1]] + [0]
                    )  # makebg transparent on last row

                if alpha == False:
                    pixel_fg = tuple(pixel_fg[:-1] + (255,))
                    pixel_bg = tuple(pixel_bg[:-1] + (255,))
                if pixel_fg[-1] == 0 and pixel_bg[-1] == 0:
                    ascii_str += f"{reset_char}{transparent_char}"
                elif pixel_fg[-1] == 0:
                    ascii_str += f"{reset_char}{palette.pixel_to_color(pixel_fg=pixel_bg, pixel_bg=pixel_bg)}"
                    if palette != Palettes.ascii:
                        ascii_str += unicode_lower_char
                else:
                    ascii_str += f"{reset_char}{palette.pixel_to_color(pixel_fg=pixel_fg, pixel_bg=pixel_bg)}"
                    if palette != Palettes.ascii:
                        ascii_str += unicode_upper_char
            else:
                continue

            if j == img.width - 1:
                ascii_str += reset_char + "\n"
    return ascii_str
