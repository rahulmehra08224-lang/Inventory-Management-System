"""
================================================================================
UNIT TESTS: ACCESSIBILITY SUITE & WCAG AAA CONTRAST ENGINE (Q12)
STUDENT: RAHUL MEHRA | CSE AIML (SECTION B)
================================================================================
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ui.theme import ThemeEngine


def hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
    """Converts #RRGGBB hex code to RGB tuple."""
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


def calculate_relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculates WCAG 2.1 relative luminance for an sRGB color."""
    normalized = []
    for val in rgb:
        s = val / 255.0
        if s <= 0.03928:
            normalized.append(s / 12.92)
        else:
            normalized.append(((s + 0.055) / 1.055) ** 2.4)
    r, g, b = normalized
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def calculate_contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculates WCAG 2.1 contrast ratio between two hex colors."""
    lum1 = calculate_relative_luminance(hex_to_rgb(hex1))
    lum2 = calculate_relative_luminance(hex_to_rgb(hex2))
    brightest = max(lum1, lum2)
    darkest = min(lum1, lum2)
    return (brightest + 0.05) / (darkest + 0.05)


class TestAccessibilitySuite(unittest.TestCase):

    def setUp(self):
        self.theme = ThemeEngine()

    def test_default_state(self):
        self.assertEqual(self.theme.font_scale, 1.0)
        self.assertFalse(self.theme.dark_mode)
        self.assertFalse(self.theme.high_contrast)
        self.assertFalse(self.theme.minimalist)
        self.assertEqual(self.theme.get_palette_key(), "light_normal")

    def test_font_resizing_engine(self):
        # Initial 1.0
        self.assertEqual(self.theme.font_scale, 1.0)

        # Step up (+1)
        scale1 = self.theme.step_font_scale(1)
        self.assertEqual(scale1, 1.20)

        # Step up again (+1)
        scale2 = self.theme.step_font_scale(1)
        self.assertEqual(scale2, 1.40)

        # Step up to maximum (1.60)
        scale3 = self.theme.step_font_scale(1)
        self.assertEqual(scale3, 1.60)

        # Clamping at max: stepping up again stays at 1.60
        scale4 = self.theme.step_font_scale(1)
        self.assertEqual(scale4, 1.60)

        # Step down to min (0.80)
        for _ in range(10):
            self.theme.step_font_scale(-1)
        self.assertEqual(self.theme.font_scale, 0.80)

        # Reset to default
        reset_scale = self.theme.reset_font_scale()
        self.assertEqual(reset_scale, 1.0)

    def test_dark_mode_toggle(self):
        self.assertFalse(self.theme.dark_mode)
        is_dark = self.theme.toggle_theme()
        self.assertTrue(is_dark)
        self.assertEqual(self.theme.get_palette_key(), "dark_normal")

        # Toggle back
        is_dark = self.theme.toggle_theme()
        self.assertFalse(is_dark)
        self.assertEqual(self.theme.get_palette_key(), "light_normal")

    def test_high_contrast_mode_toggle(self):
        self.assertFalse(self.theme.high_contrast)
        is_high = self.theme.toggle_contrast()
        self.assertTrue(is_high)
        self.assertEqual(self.theme.get_palette_key(), "light_high_contrast")

        # Combine with dark mode
        self.theme.toggle_theme()
        self.assertEqual(self.theme.get_palette_key(), "dark_high_contrast")

    def test_minimalist_layout_toggle(self):
        self.assertFalse(self.theme.minimalist)
        is_minimal = self.theme.toggle_minimalist()
        self.assertTrue(is_minimal)

    def test_wcag_aaa_contrast_ratio_validation(self):
        """
        Mathematical verification that High Contrast modes meet or exceed
        the WCAG 2.1 Level AAA requirement (>= 7.0:1 for normal text).
        """
        # 1. High Contrast Light: Pure black (#000000) on Pure White (#ffffff)
        light_hc = self.theme.PALETTES["light_high_contrast"]
        ratio_light = calculate_contrast_ratio(light_hc["fg"], light_hc["bg"])
        self.assertGreaterEqual(ratio_light, 7.0)
        self.assertAlmostEqual(ratio_light, 21.0, places=1)  # Maximum possible 21:1

        # 2. High Contrast Dark: Pure White (#ffffff) on Pure OLED Black (#000000)
        dark_hc = self.theme.PALETTES["dark_high_contrast"]
        ratio_dark = calculate_contrast_ratio(dark_hc["fg"], dark_hc["bg"])
        self.assertGreaterEqual(ratio_dark, 7.0)
        self.assertAlmostEqual(ratio_dark, 21.0, places=1)

        # 3. High Contrast Dark Accent: Yellow (#ffe600) on Pure Black (#000000)
        ratio_accent = calculate_contrast_ratio(dark_hc["primary"], dark_hc["bg"])
        self.assertGreaterEqual(ratio_accent, 7.0)  # ~17.5:1 ratio


if __name__ == "__main__":
    unittest.main()
