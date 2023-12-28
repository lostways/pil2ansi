# Pil2ANSI
Library for converting Pillow images to ANSI art

![pil2ansi3](https://github.com/lostways/pil2ansi/assets/1101232/f92f210f-5e08-4a59-831d-47d6d9aa5c59)

# Getting Started

## Installation
```
pip install pil2ansi
```

## Examples
Check out the [Convert Image Example](https://github.com/lostways/pil2ansi/blob/master/examples/convert_img.py).
```
convert_img.py [-h] [--palette {color,grayscale,grayscale_inverted,ascii}] [--width WIDTH] [--no-alpha] img_path
```

# Usage

## Convert any PIL image to ANSI art
```python
from PIL import Image
from pil2ansi import convert_img

# Open the image
img = Image.open("path/to/image.png")

# Convert to ANSI
ansi_img = convert_img(img)

# Print to screen
print(ansi_img) 
```

## Palettes
There are a few palettes to choose from. To select a palette import `Palettes` and then pass the one you want into the `convert_img` function.

```python
from PIL import Image
from pil2ansi import convert_img, Palettes

# Open the image
img = Image.open("path/to/image.png")

# Convert to ANSI
ansi_img = convert_img(img, palette=Palettes.acsii)

# Print to screen
print(ansi_img) 
```

The default palette is `color`. You can choose from `color`, `grayscale`, `grayscale_inverted`, and `ascii`.

## Resizing the image
By default the image will crop to the width of your terminal widow. You can change the width of the output by passing `width` to `convert_img`. This width is the number of columns you want the image to fit in your terminal window. The aspect radio of the original image will be preserved.

```python
from PIL import Image
from pil2ansi import convert_img

# Open the image
img = Image.open("path/to/image.png")

# Convert to ANSI
ansi_img = convert_img(img, width=100)

# Print to screen
print(ansi_img) 
```

## Transparency
By default any part of the image with an alpha of 0 will be converted to a ` `, rendering it transparent. You can turn this off by setting `alpha` to `False` in `convert_img`.

```python
from PIL import Image
from pil2ansi import convert_img

# Open the image
img = Image.open("path/to/image.png")

# Convert to ANSI
ansi_img = convert_img(img, alpha=False)

# Print to screen
print(ansi_img) 
```

# Development
Install all dependencies including dev dependencies by running `make dev`

Run tests with `make test`

Run `mypy` and `black` checks with `make lint`
