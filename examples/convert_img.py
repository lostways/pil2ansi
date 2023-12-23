import argparse
from pathlib import Path
from PIL import Image
from pil2ansi import convert_img, Palettes

parser = argparse.ArgumentParser(description='Convert image file to ANSI')
parser.add_argument('img_path', help='path to image file')
args = parser.parse_args()

# get the image
img_path = Path(args.img_path).as_posix()
img = Image.open(img_path)

# convert to ansi
out = convert_img(img, alpha=True)

# print to terminal
print(out)
