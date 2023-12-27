from pil2ansi import convert_img, Palettes
from PIL import Image

class TestConvertImg:
    reset_char: str = "\033[0m"
    transparent_char: str = f"{reset_char} "
    unicode_upper_char: str = "\u2580"
    unicode_lower_char: str = "\u2584"

    RGBA_red_out: str = f"{reset_char}\033[38;2;255;0;0;48;2;255;0;0m{unicode_upper_char}"
    RGBA_red_end_row_out: str = f"{reset_char}\033[38;2;255;0;0;48;1m{unicode_upper_char}"
    RGBA_red_alpha_upper_out: str = f"{reset_char}\033[38;2;255;0;0;48;1m{unicode_lower_char}"
    RGBA_red_alpha_lower_out: str = f"{reset_char}\033[38;2;255;0;0;48;1m{unicode_upper_char}"

    LA_red_out: str = f"{reset_char}\033[38;5;238;48;5;238m{unicode_upper_char}"
    LA_red_end_row_out: str = f"{reset_char}\033[38;5;238;48;1m{unicode_upper_char}"
    LA_red_alpha_upper_out: str = f"{reset_char}\033[38;5;238;48;1m{unicode_lower_char}"
    LA_red_alpha_lower_out: str = f"{reset_char}\033[38;5;238;48;1m{unicode_upper_char}"

    end_row_out: str = f"{reset_char}\n"

    def test_convert_img_color_2x2(self):
        img: Image.Image = Image.new("RGBA", (2, 2), (255, 0, 0, 255))
        expected_out: str = self.RGBA_red_out * 2 + self.end_row_out
        out = convert_img(img, Palettes.color)

        assert len(img.getdata()) == 4
        assert img.width == 2
        assert out == expected_out

    def test_convert_img_color_4x4(self):
        img: Image.Image = Image.new("RGBA", (4, 4), (255, 0, 0, 255))
        expected_out: str = (self.RGBA_red_out * 4 + self.end_row_out) * 2
        out = convert_img(img, Palettes.color)

        assert len(img.getdata()) == 16
        assert img.width == 4
        assert out == expected_out

    def test_convert_img_color_5x7(self):
        img: Image.Image = Image.new("RGBA", (5, 7), (255, 0, 0, 255))
        expected_out: str = (self.RGBA_red_out * 5 + self.end_row_out) * 3
        expected_out += self.RGBA_red_end_row_out * 5 + self.end_row_out
        out = convert_img(img, Palettes.color)

        assert len(img.getdata()) == 35
        assert img.width == 5
        assert out == expected_out

    def test_convert_img_color_alpha_4x4(self):
        img: Image.Image = Image.new("RGBA", (4, 4), (255, 0, 0, 255))
        img.putpixel((0, 0), (255, 0, 0, 0))
        img.putpixel((0, 3), (255, 0, 0, 0))
        img.putpixel((3, 0), (255, 0, 0, 0))
        img.putpixel((3, 3), (255, 0, 0, 0))

        expected_out: str = (
            self.RGBA_red_alpha_upper_out 
            + (self.RGBA_red_out * 2) 
            + self.RGBA_red_alpha_upper_out  
            + self.end_row_out
        )
        expected_out += (
            self.RGBA_red_alpha_lower_out 
            + (self.RGBA_red_out * 2) 
            + self.RGBA_red_alpha_lower_out 
            + self.end_row_out
        )
        out = convert_img(img, Palettes.color, alpha=True)

        assert len(img.getdata()) == 16
        assert img.width == 4
        assert out == expected_out

    def test_convert_img_color_alpha_5x7(self):
        img: Image.Image = Image.new("RGBA", (5, 7), (255, 0, 0, 255))
        img.putpixel((0, 0), (255, 0, 0, 0))
        img.putpixel((0, 6), (255, 0, 0, 0))
        img.putpixel((4, 0), (255, 0, 0, 0))
        img.putpixel((4, 6), (255, 0, 0, 0))

        expected_out: str = (
            self.RGBA_red_alpha_upper_out 
            + (self.RGBA_red_out * 3) 
            + self.RGBA_red_alpha_upper_out  
            + self.end_row_out
        )
        expected_out += (
            (self.RGBA_red_out * 5) 
            + self.end_row_out
        ) * 2
        expected_out += (
            self.transparent_char
            + (self.RGBA_red_alpha_lower_out * 3) 
            + self.transparent_char
            + self.end_row_out
        )
        out = convert_img(img, Palettes.color, alpha=True)
        print(repr(expected_out))
        print("\n")
        print(repr(out))
        print(expected_out)
        print("\n")
        print(out)

        assert len(img.getdata()) == 35
        assert img.width == 5
        assert out == expected_out

    def test_convert_img_grayscale_2x2(self):
        img: Image.Image = Image.new("RGBA", (2, 2), (255, 0, 0, 255))
        expected_out: str = self.LA_red_out * 2 + self.end_row_out
        out = convert_img(img, Palettes.grayscale)

        assert len(img.getdata()) == 4
        assert img.width == 2
        assert out == expected_out



