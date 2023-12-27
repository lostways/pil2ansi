from pil2ansi import PaletteAscii, PaletteColor, PaletteGrayscale


class TestPaletteAscii:
    def test_init(self):
        palette = PaletteAscii()
        assert palette.pil_color == "LA"
        assert palette.palette_chars == [".", ",", ":", "+", "*", "?", "%", "@"]

    def test_pixel_to_color(self):
        palette = PaletteAscii()
        assert palette.pixel_to_color((0, 255), (0, 0)) == "."
        assert palette.pixel_to_color((255, 255), (0, 0)) == "@"
        assert palette.pixel_to_color((127, 255), (0, 0)) == "+"
        assert palette.pixel_to_color((127, 0), (0, 255)) == "."
        assert palette.pixel_to_color((127, 0), (255, 255)) == "@"
        assert palette.pixel_to_color((127, 0), (127, 255)) == "+"


class TestPaletteGrayscale:
    def test_init(self):
        palette = PaletteGrayscale()
        assert palette.pil_color == "LA"
        assert palette.invert == False

    def test_pixel_to_color(self):
        palette = PaletteGrayscale()
        assert palette.pixel_to_color((0, 255), (127, 255)) == "\033[38;5;232;48;5;243m"
        assert palette.pixel_to_color((255, 255), (127, 255)) == "\033[38;5;255;48;5;243m"
        assert palette.pixel_to_color((127, 255), (127, 255)) == "\033[38;5;243;48;5;243m"
        assert palette.pixel_to_color((127, 0), (127, 255)) == "\033[38;1;48;5;243m"
        assert palette.pixel_to_color((0, 255), (127, 0)) == "\033[38;5;232;48;1m"

    def test_pixel_to_char_inverted(self):
        palette = PaletteGrayscale(invert=True)
        assert palette.pixel_to_color((0, 255), (127, 255)) == "\033[38;5;255;48;5;244m"
        assert palette.pixel_to_color((255, 255), (127, 255)) == "\033[38;5;232;48;5;244m"
        assert palette.pixel_to_color((127, 255), (127, 255)) == "\033[38;5;244;48;5;244m"
        assert palette.pixel_to_color((127, 0), (127, 255)) == "\033[38;1;48;5;244m"
        assert palette.pixel_to_color((0, 255), (127, 0)) == "\033[38;5;255;48;1m"


class TestPaletteColor:
    def test_init(self):
        palette = PaletteColor()
        assert palette.pil_color == "RGBA"

    def test_pixel_to_char(self):
        palette = PaletteColor()

        assert (
            palette.pixel_to_color((255, 127, 255, 255), (255, 255, 0, 255))
            == "\033[38;2;255;127;255;48;2;255;255;0m"
        )

        assert (
            palette.pixel_to_color((255, 127, 255, 0), (255, 255, 0, 255))
            == "\033[38;1;48;2;255;255;0m"
        )

        assert (
            palette.pixel_to_color((255, 127, 255, 255), (255, 255, 0, 0))
            == "\033[38;2;255;127;255;48;1m"
        )
