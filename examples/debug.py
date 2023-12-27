from pil2ansi import convert_img, Palettes, Palette
from PIL import Image

palettes: list = [Palettes.color, Palettes.grayscale, Palettes.grayscale_inverted, Palettes.ascii]
reset: str = "\033[0m"

def print_palette(palette: Palette):
    print(f"\nPalette: {palette.__class__.__name__}")
    if palette.pil_color == "LA":
        for i in range(256):
            print(f"{reset}{palette.pixel_to_color((i, 255), (i, 255))} {reset}", end="")
            if (i + 1) % (256 / 4) == 0:
                print("\n", end="")
    else:
        for i in range(256):
            print(f"{reset}{palette.pixel_to_color((i, 0, 0, 255), (i, 0, 0, 255))} {reset}", end="")
            if (i + 1) % (256 / 4) == 0:
                print("\n", end="")
        for i in range(256):
            print(f"{reset}{palette.pixel_to_color((0, i, 0, 255), (0, i, 0, 255))} {reset}", end="")
            if (i + 1) % (256 / 4) == 0:
                print("\n", end="")
        for i in range(256):
            print(f"{reset}{palette.pixel_to_color((0, 0, i, 255), (0, 0, i, 255))} {reset}", end="")
            if (i + 1) % (256 / 4) == 0:
                print("\n", end="")

for palette in palettes: print_palette(palette)

# 2x2
img_2x2: Image.Image = Image.new("RGBA", (2, 2), (255, 0, 0, 255))

# 4x4
img_4x4: Image.Image = Image.new("RGBA", (4, 4), (255, 0, 0, 255))

# 4x4 with transparent corners
img_4x4_alpha: Image.Image = Image.new("RGBA", (4, 4), (255, 0, 0, 255))
img_4x4_alpha.putpixel((0, 0), (255, 0, 0, 0))
img_4x4_alpha.putpixel((0, 3), (255, 0, 0, 0))
img_4x4_alpha.putpixel((3, 0), (255, 0, 0, 0))
img_4x4_alpha.putpixel((3, 3), (255, 0, 0, 0))

# 5x7
img_5x7: Image.Image = Image.new("RGBA", (5, 7), (255, 0, 0, 255))

# 5x7 with transparent corners
img_5x7_alpha: Image.Image = Image.new("RGBA", (5, 7), (255, 0, 0, 255))
img_5x7_alpha.putpixel((0, 0), (255, 0, 0, 0))
img_5x7_alpha.putpixel((0, 6), (255, 0, 0, 0))
img_5x7_alpha.putpixel((4, 0), (255, 0, 0, 0))
img_5x7_alpha.putpixel((4, 6), (255, 0, 0, 0))


print("\n2x2")
for palette in palettes: print(convert_img(img_2x2, palette))

print("\n4x4")
for palette in palettes: print(convert_img(img_4x4, palette))

print("\n5x7")
for palette in palettes: print(convert_img(img_5x7, palette))

print("\n4x4 with transparent corners")
for palette in palettes: print(convert_img(img_4x4_alpha, palette))

print("\n5x7 with transparent corners")
for palette in palettes: print(convert_img(img_5x7_alpha, palette))

