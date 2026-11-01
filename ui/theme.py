"""
================================================================================
BBAT104: ACCESSIBILITY & THEME ENGINE (Q12 IMPLEMENTATION)
STUDENT: RAHUL MEHRA | CSE AIML (SECTION B)
FEATURES: HIGH CONTRAST, FONT RESIZING, DARK MODE, MINIMALIST COGNITIVE LAYOUT
================================================================================
"""

class ThemeEngine:
    """Manages color palettes, typography scaling, and cognitive display states."""

    PALETTES = {
        "light_normal": {
            "name": "Standard Light",
            "bg": "#f8fafc",
            "surface": "#ffffff",
            "surface_alt": "#f1f5f9",
            "fg": "#0f172a",
            "fg_muted": "#475569",
            "primary": "#2563eb",
            "primary_hover": "#1d4ed8",
            "primary_fg": "#ffffff",
            "border": "#cbd5e1",
            "select_bg": "#dbeafe",
            "select_fg": "#1e3a8a",
            "danger": "#b91c1c",
            "danger_bg": "#fee2e2",
            "warning": "#b45309",
            "warning_bg": "#fef3c7",
            "success": "#15803d",
            "success_bg": "#dcfce7",
            "focus_ring": "#2563eb",
            "card_bd": 1
        },
        "dark_normal": {
            "name": "Standard Dark",
            "bg": "#0b1120",
            "surface": "#1e293b",
            "surface_alt": "#0f172a",
            "fg": "#f8fafc",
            "fg_muted": "#94a3b8",
            "primary": "#3b82f6",
            "primary_hover": "#60a5fa",
            "primary_fg": "#ffffff",
            "border": "#334155",
            "select_bg": "#1e3a8a",
            "select_fg": "#ffffff",
            "danger": "#f87171",
            "danger_bg": "#7f1d1d",
            "warning": "#fde047",
            "warning_bg": "#78350f",
            "success": "#4ade80",
            "success_bg": "#064e3b",
            "focus_ring": "#60a5fa",
            "card_bd": 1
        },
        "light_high_contrast": {
            "name": "High Contrast Light (WCAG AAA)",
            "bg": "#ffffff",
            "surface": "#ffffff",
            "surface_alt": "#f0f0f0",
            "fg": "#000000",
            "fg_muted": "#111111",
            "primary": "#000000",
            "primary_hover": "#222222",
            "primary_fg": "#ffffff",
            "border": "#000000",
            "select_bg": "#000000",
            "select_fg": "#ffffff",
            "danger": "#900000",
            "danger_bg": "#ffffff",
            "warning": "#000000",
            "warning_bg": "#ffffff",
            "success": "#000000",
            "success_bg": "#ffffff",
            "focus_ring": "#000000",
            "card_bd": 2
        },
        "dark_high_contrast": {
            "name": "High Contrast Dark (OLED Black)",
            "bg": "#000000",
            "surface": "#000000",
            "surface_alt": "#141414",
            "fg": "#ffffff",
            "fg_muted": "#ffffff",
            "primary": "#ffe600",
            "primary_hover": "#fff275",
            "primary_fg": "#000000",
            "border": "#ffffff",
            "select_bg": "#ffe600",
            "select_fg": "#000000",
            "danger": "#ff4d4d",
            "danger_bg": "#000000",
            "warning": "#ffe600",
            "warning_bg": "#000000",
            "success": "#00ff66",
            "success_bg": "#000000",
            "focus_ring": "#ffe600",
            "card_bd": 2
        }
    }

    # Allowed font scaling steps (80% to 160%)
    FONT_SCALES = [0.80, 1.0, 1.20, 1.40, 1.60]

    def __init__(self):
        self.font_scale = 1.0
        self.dark_mode = False
        self.high_contrast = False
        self.minimalist = False

    def get_palette_key(self) -> str:
        if self.high_contrast:
            return "dark_high_contrast" if self.dark_mode else "light_high_contrast"
        else:
            return "dark_normal" if self.dark_mode else "light_normal"

    def get_palette(self) -> dict:
        return self.PALETTES[self.get_palette_key()]

    def get_font(self, size_pt: int, weight: str = "normal") -> tuple:
        """Returns font tuple with dynamic scale multiplier."""
        scaled_size = max(8, int(round(size_pt * self.font_scale)))
        return ("Segoe UI", scaled_size, weight)

    def step_font_scale(self, direction: int) -> float:
        """Increases (+1) or decreases (-1) font scale by predefined step."""
        current_idx = min(
            range(len(self.FONT_SCALES)),
            key=lambda i: abs(self.FONT_SCALES[i] - self.font_scale)
        )
        new_idx = max(0, min(len(self.FONT_SCALES) - 1, current_idx + direction))
        self.font_scale = self.FONT_SCALES[new_idx]
        return self.font_scale

    def reset_font_scale(self) -> float:
        self.font_scale = 1.0
        return self.font_scale

    def toggle_theme(self) -> bool:
        self.dark_mode = not self.dark_mode
        return self.dark_mode

    def toggle_contrast(self) -> bool:
        self.high_contrast = not self.high_contrast
        return self.high_contrast

    def toggle_minimalist(self) -> bool:
        self.minimalist = not self.minimalist
        return self.minimalist
