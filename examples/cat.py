from pathlib import Path
from pil2ansi import convert_img
img_path = Path.joinpath(Path(__file__).parent,'imgs/cat.png').as_posix()

out = convert_img(img_path)
print(out)
