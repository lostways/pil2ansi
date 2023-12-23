import argparse
from pathlib import Path
from pil2ansi import convert_img, Palettes

parser = argparse.ArgumentParser(description='Convert image file to ANSI')
parser.add_argument('img_path', help='path to image file')
args = parser.parse_args()

img_path = Path(args.img_path).as_posix()
out = convert_img(img_path, alpha=True)
print(out)
