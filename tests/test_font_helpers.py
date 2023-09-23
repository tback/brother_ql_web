from unittest import TestCase

from brother_ql_web.font_helpers import get_fonts


class GetFontsTestCase(TestCase):
    # Reference: https://packages.ubuntu.com/lunar/all/fonts-roboto-unhinted/filelist
    ROBOTO_FILES = {
        "Roboto": {
            "Thin": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Thin.ttf",
            "Medium Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-MediumItalic.ttf",
            "Thin Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-ThinItalic.ttf",
            "Light Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-LightItalic.ttf",
            "Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Italic.ttf",
            "Black Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-BlackItalic.ttf",
            "Medium": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Medium.ttf",
            "Bold": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Bold.ttf",
            "Black": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf",
            "Light": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Light.ttf",
            "Regular": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Regular.ttf",
            "Bold Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-BoldItalic.ttf",
        },
        "Roboto Black": {
            "Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-BlackItalic.ttf",
            "Regular": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf",
        },
        "Roboto Condensed": {
            "Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Italic.ttf",
            "Bold": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf",
            "Medium": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Medium.ttf",
            "Bold Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-BoldItalic.ttf",
            "Light Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-LightItalic.ttf",
            "Light": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Light.ttf",
            "Medium Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-MediumItalic.ttf",
            "Regular": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Regular.ttf",
        },
        "Roboto Condensed Light": {
            "Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-LightItalic.ttf",
            "Regular": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Light.ttf",
        },
        "Roboto Condensed Medium": {
            "Regular": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Medium.ttf",
            "Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-MediumItalic.ttf",
        },
        "Roboto Light": {
            "Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-LightItalic.ttf",
            "Regular": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Light.ttf",
        },
        "Roboto Medium": {
            "Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-MediumItalic.ttf",
            "Regular": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Medium.ttf",
        },
        "Roboto Thin": {
            "Regular": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Thin.ttf",
            "Italic": "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-ThinItalic.ttf",
        },
    }

    def assert_font_dictionary_subset(self, expected, actual, not_in_name: str = ""):
        for font_name, font_styles in expected.items():
            self.assertIn(font_name, actual)
            actual_styles = actual[font_name]
            with self.subTest(font_name=font_name):
                for font_style, path in font_styles.items():
                    self.assertIn(font_style, actual_styles)
                    self.assertEqual(path, actual_styles[font_style], font_style)
            if not_in_name:
                self.assertNotIn(not_in_name, font_name)

    def test_get_all(self):
        fonts = get_fonts()
        self.assert_font_dictionary_subset(expected=self.ROBOTO_FILES, actual=fonts)

    def test_get_from_folder(self):
        fonts = get_fonts(folder="/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF")
        expected = {
            key: value
            for key, value in self.ROBOTO_FILES.items()
            if "Condensed" not in key
        }
        self.assert_font_dictionary_subset(
            expected=expected, actual=fonts, not_in_name="Condensed"
        )
