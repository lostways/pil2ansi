from pil2ansi import PaletteAscii, PaletteColor, PaletteGrayscale


class TestPaletteAscii:
    def test_init(self):
        palette = PaletteAscii()
        assert palette.pil_color == "LA"
        assert palette.palette_chars == [".", ",", ":", "+", "*", "?", "%", "@"]

    def test_pixel_to_char(self):
        palette = PaletteAscii()
        assert palette.pixel_to_char((0, 0)) == "."
        assert palette.pixel_to_char((255, 0)) == "@"
        assert palette.pixel_to_char((127, 0)) == "+"
    
class TestPaletteGrayscale:
    def test_init(self):
        palette = PaletteGrayscale()
        assert palette.pil_color == "LA"
        assert palette.invert == False

    def test_pixel_to_char(self):
        palette = PaletteGrayscale()
        assert palette.pixel_to_char((0, 0)) == "\033[0;48;5;232m \033[0m"
        assert palette.pixel_to_char((255, 0)) == "\033[0;48;5;255m \033[0m"
        assert palette.pixel_to_char((127, 0)) == "\033[0;48;5;243m \033[0m"

    def test_pixel_to_char_inverted(self):
        palette = PaletteGrayscale(invert=True)
        assert palette.pixel_to_char((0, 0)) == "\033[0;48;5;255m \033[0m"
        assert palette.pixel_to_char((255, 0)) == "\033[0;48;5;232m \033[0m"
        assert palette.pixel_to_char((127, 0)) == "\033[0;48;5;244m \033[0m"

class TestPaletteColor:
    def test_init(self):
        palette = PaletteColor()
        assert palette.pil_color == "RGBA"

    def test_pixel_to_char(self):
        palette = PaletteColor()
        assert palette.pixel_to_char((0, 0, 0, 0)) == "\033[0;48;2;0;0;0m \033[0m"
        assert palette.pixel_to_char((255, 0, 0, 0)) == "\033[0;48;2;255;0;0m \033[0m"
        assert palette.pixel_to_char((127, 0, 0, 0)) == "\033[0;48;2;127;0;0m \033[0m"
