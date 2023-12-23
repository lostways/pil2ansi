import sys
from pathlib import Path
from pil2ansi import convert_img, Palettes
img_path = Path(sys.argv[1]).as_posix()

out = convert_img(img_path, Palettes.color, alpha=True)
print(out)
