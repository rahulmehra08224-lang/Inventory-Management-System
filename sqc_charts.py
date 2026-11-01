"""
================================================================================
BBAT104: STATISTICAL QUALITY CONTROL (SQC) CHART GENERATOR
STUDENT: RAHUL MEHRA | CSE AIML (SECTION B)
BASELINE: INVENTORY MANAGEMENT SYSTEM (DIGIT 3) - Q12 ACCESSIBILITY
CHARTS GENERATED:
  1. PARETO CHART (80/20 RULE) - DEFECT OCCURRENCE & CUMULATIVE PERCENTAGE
  2. ISHIKAWA (FISHBONE) ROOT CAUSE DIAGRAM (PEOPLE, PROCESS, CODE, ENVIRONMENT)
================================================================================
"""

import os
import sys

# Output directory for SQC charts
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sampled Defect Data from Laboratory Audit (50 items)
DEFECT_DATA = [
    ("Unnotified Stockouts", 18),
    ("Low Contrast Inaccessibility", 12),
    ("Manual Count Drift", 9),
    ("Keyboard Tab Nav Trap", 5),
    ("Duplicate SKU Insertion", 3),
    ("Turnover Calculation Lag", 2),
    ("Missing Specs Detail", 1)
]


def generate_pareto_matplotlib():
    """Generates Pareto Chart using Matplotlib and saves to PNG."""
    try:
        import matplotlib
        matplotlib.use("Agg")  # Non-interactive backend
        import matplotlib.pyplot as plt

        categories = [item[0] for item in DEFECT_DATA]
        counts = [item[1] for item in DEFECT_DATA]
        total = sum(counts)

        cumulative = []
        running = 0
        for c in counts:
            running += c
            cumulative.append((running / total) * 100)

        fig, ax1 = plt.subplots(figsize=(10, 6), dpi=150)

        # Primary Bar Chart (Frequencies)
        bars = ax1.bar(categories, counts, color="#2563eb", edgecolor="#1e40af", width=0.6, label="Defect Count")
        ax1.set_ylabel("Defect Frequency (Count)", color="#1e40af", fontsize=11, fontweight="bold")
        ax1.tick_params(axis="y", labelcolor="#1e40af")
        ax1.set_ylim(0, 22)

        # Annotate bar counts
        for bar in bars:
            yval = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.4, int(yval), ha="center", va="bottom", fontsize=10, fontweight="bold")

        plt.xticks(rotation=30, ha="right", fontsize=9)

        # Secondary Cumulative Line Chart
        ax2 = ax1.twinx()
        ax2.plot(categories, cumulative, color="#dc2626", marker="D", linewidth=2.5, markersize=6, label="Cumulative %")
        ax2.set_ylabel("Cumulative Percentage (%)", color="#dc2626", fontsize=11, fontweight="bold")
        ax2.tick_params(axis="y", labelcolor="#dc2626")
        ax2.set_ylim(0, 110)

        # 80% Cutoff line
        ax2.axhline(80, color="#b91c1c", linestyle="--", linewidth=1.5, label="80% Pareto Cutoff")
        ax2.text(len(categories) - 1.2, 82, "80% Cutoff (Vital Few)", color="#b91c1c", fontweight="bold", fontsize=10)

        # Annotate cumulative percentages
        for i, txt in enumerate(cumulative):
            ax2.annotate(f"{txt:.0f}%", (categories[i], cumulative[i] - 5), ha="center", color="#dc2626", fontsize=9, fontweight="bold")

        plt.title("BBAT104 SQC: Pareto Analysis of Inventory & Accessibility Defects (80/20 Rule)\nStudent: Rahul Mehra (CSE AIML Sec B)", fontsize=12, fontweight="bold", pad=15)
        plt.tight_layout()

        png_path = os.path.join(OUTPUT_DIR, "pareto_chart.png")
        plt.savefig(png_path)
        plt.close()
        print(f"[OK] Saved Matplotlib Pareto Chart: {png_path}")
        return png_path
    except ImportError:
        print("Notice: Matplotlib not installed; generating SVG fallback.")
        return None


def generate_fishbone_matplotlib():
    """Generates Ishikawa (Fishbone) Diagram using Matplotlib annotations."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")

        # Central Spine
        ax.annotate(
            "",
            xy=(8.2, 5),
            xytext=(0.5, 5),
            arrowprops=dict(arrowstyle="->", color="#0f172a", lw=4)
        )

        # Problem Effect Box (Head)
        bbox_head = dict(boxstyle="round,pad=0.5", facecolor="#fee2e2", edgecolor="#dc2626", lw=2)
        ax.text(
            8.4, 5,
            "PROBLEM EFFECT:\nInventory Stockouts\n& Inaccessibility",
            ha="left", va="center", fontsize=11, fontweight="bold", color="#991b1b", bbox=bbox_head
        )

        # 4 Main Bones (People, Process, Code, Environment)
        bones = [
            ("1. PEOPLE", 2.2, 7.8, 3.5, 5.0, [("No Accessibility Training", 2.0, 7.0), ("Manual Count Oversight", 2.4, 6.2)]),
            ("2. PROCESS", 5.2, 7.8, 6.5, 5.0, [("Delayed Reorder Triggers", 5.0, 7.0), ("No Statistical Safety Stock", 5.4, 6.2)]),
            ("3. SOFTWARE CODE", 2.2, 2.2, 3.5, 5.0, [("Low-Contrast Gray Themes", 2.0, 3.0), ("Missing Focus Traps", 2.4, 3.8)]),
            ("4. ENVIRONMENT", 5.2, 2.2, 6.5, 5.0, [("Ambient Room Glare", 5.0, 3.0), ("Disorganized Storage Bins", 5.4, 3.8)])
        ]

        for title, x1, y1, x2, y2, sub_causes in bones:
            color = "#2563eb" if y1 > 5 else "#16a34a"
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", color=color, lw=2.5))
            ax.text(x1, y1, title, ha="center", va="center", fontsize=11, fontweight="bold",
                    color=color, bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor=color, lw=1.5))

            for sub_text, sx, sy in sub_causes:
                ax.text(sx, sy, f"• {sub_text}", fontsize=8.5, color="#334155")

        plt.title("BBAT104 SQC: Ishikawa (Fishbone) Root Cause Diagram\nStudent: Rahul Mehra | CSE AIML (Sec B) | Digit 3 (Inventory) - Q12 Accessibility", fontsize=12, fontweight="bold", pad=12)
        plt.tight_layout()

        png_path = os.path.join(OUTPUT_DIR, "fishbone_diagram.png")
        plt.savefig(png_path)
        plt.close()
        print(f"[OK] Saved Matplotlib Fishbone Diagram: {png_path}")
        return png_path
    except ImportError:
        print("Notice: Matplotlib not installed; generating SVG fallback.")
        return None


def generate_pure_svg_fallbacks():
    """Generates standalone pure SVG vector files without external dependencies."""
    from sqc_tools import generate_pareto_svg, generate_fishbone_svg
    svg1 = os.path.join(OUTPUT_DIR, "pareto_chart.svg")
    svg2 = os.path.join(OUTPUT_DIR, "fishbone_diagram.svg")
    generate_pareto_svg(svg1)
    generate_fishbone_svg(svg2)
    print(f"[OK] Saved Pure SVG Pareto: {svg1}")
    print(f"[OK] Saved Pure SVG Fishbone: {svg2}")


def main():
    print("=" * 65)
    print("BBAT104 SQC Chart Generator (Rahul Mehra - CSE AIML Sec B)")
    print("=" * 65)
    generate_pareto_matplotlib()
    generate_fishbone_matplotlib()
    generate_pure_svg_fallbacks()
    print("All SQC Charts successfully generated in docs/images/")


if __name__ == "__main__":
    main()
