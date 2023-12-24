import argparse
from pathlib import Path
from PIL import Image
from pil2ansi import convert_img, Palettes

parser = argparse.ArgumentParser(description="Convert image file to ANSI")
parser.add_argument("img_path", help="path to image file")
parser.add_argument(
    "--palette",
    help="palette to use",
    choices=["color", "grayscale", "grayscale_inverted", "ascii"],
    default="color",
)
parser.add_argument("--width", help="width of output", type=int, default=-1)
parser.add_argument("--alpha", help="enable transparency", action="store_true")

args = parser.parse_args()

# get the image
img_path = Path(args.img_path).as_posix()
img = Image.open(img_path)

# convert to ansi
out = convert_img(
    img=img,
    palette=getattr(Palettes, args.palette),
    width=args.width,
    alpha=args.alpha,
)

# print to terminal
print(out)
