"""
================================================================================
BBAT104: STATISTICAL QUALITY CONTROL (SQC) GENERATOR
STUDENT: RAHUL MEHRA | CSE AIML (SECTION B)
ASSIGNMENT: INVENTORY MANAGEMENT SYSTEM (DIGIT 3) - Q12 ACCESSIBILITY
DELIVERABLES: PARETO ANALYSIS (80/20), ISHIKAWA (FISHBONE), DEFECT CHECKSHEET
================================================================================
"""

import os
import json

def generate_pareto_svg(output_path="pareto_chart.svg"):
    """Generates a standalone, crisp vector SVG Pareto Chart (80/20 Rule)."""
    # Defect categories from SQC Checksheet (50 sampled defects)
    categories = [
        ("Unnotified Stockouts", 18),
        ("Low Contrast Visibility", 12),
        ("Manual Count Drift", 9),
        ("Keyboard Navigation Trap", 5),
        ("Duplicate SKU Insertion", 3),
        ("Turnover Calc Lag", 2),
        ("Missing Specs Detail", 1)
    ]
    
    total = sum(count for _, count in categories)
    running_sum = 0
    cumulative_pcts = []
    for name, count in categories:
        running_sum += count
        cumulative_pcts.append((running_sum / total) * 100)

    # SVG layout
    svg_w, svg_h = 750, 450
    margin_l, margin_r, margin_t, margin_b = 60, 60, 50, 110
    plot_w = svg_w - margin_l - margin_r
    plot_h = svg_h - margin_t - margin_b

    max_count = 20
    bar_width = plot_w / len(categories) * 0.65
    bar_step = plot_w / len(categories)

    bars_svg = []
    line_points = []
    circles_svg = []
    labels_svg = []

    for i, (name, count) in enumerate(categories):
        x = margin_l + i * bar_step + (bar_step - bar_width) / 2
        h = (count / max_count) * plot_h
        y = margin_t + plot_h - h

        # Bar
        bars_svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{h:.1f}" fill="#2563eb" rx="3" stroke="#1d4ed8" stroke-width="1"/>')
        bars_svg.append(f'<text x="{x + bar_width/2:.1f}" y="{y - 6:.1f}" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">{count}</text>')

        # Category label rotated
        labels_svg.append(f'<text x="{x + bar_width/2:.1f}" y="{margin_t + plot_h + 18:.1f}" font-family="Segoe UI, sans-serif" font-size="11" fill="#334155" text-anchor="end" transform="rotate(-35 {x + bar_width/2:.1f} {margin_t + plot_h + 18:.1f})">{name}</text>')

        # Cumulative line point
        cum_x = x + bar_width / 2
        cum_y = margin_t + plot_h - (cumulative_pcts[i] / 100) * plot_h
        line_points.append(f"{cum_x:.1f},{cum_y:.1f}")
        circles_svg.append(f'<circle cx="{cum_x:.1f}" cy="{cum_y:.1f}" r="4" fill="#dc2626" stroke="#ffffff" stroke-width="2"/>')
        circles_svg.append(f'<text x="{cum_x:.1f}" y="{cum_y - 8:.1f}" font-family="Segoe UI, sans-serif" font-size="10" font-weight="bold" fill="#dc2626" text-anchor="middle">{cumulative_pcts[i]:.0f}%</text>')

    # 80% reference threshold line
    y_80 = margin_t + plot_h - (0.80 * plot_h)
    line_80_svg = f'<line x1="{margin_l}" y1="{y_80:.1f}" x2="{margin_l + plot_w}" y2="{y_80:.1f}" stroke="#dc2626" stroke-dasharray="5,5" stroke-width="2"/>'
    line_80_svg += f'<text x="{margin_l + plot_w + 5}" y="{y_80 + 4:.1f}" font-family="Segoe UI, sans-serif" font-size="11" font-weight="bold" fill="#dc2626">80% Cutoff</text>'

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
      <rect width="100%" height="100%" fill="#ffffff" rx="8"/>
      <text x="{svg_w / 2}" y="30" font-family="Segoe UI, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">
        Pareto Analysis of Inventory & Accessibility Defects (80/20 Rule)
      </text>
      <text x="{svg_w / 2}" y="45" font-family="Segoe UI, sans-serif" font-size="11" fill="#64748b" text-anchor="middle">
        BBAT104 TQM Coursework • Student: Rahul Mehra (CSE AIML Sec B)
      </text>

      <!-- Axes -->
      <line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{margin_t + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>
      <line x1="{margin_l}" y1="{margin_t + plot_h}" x2="{margin_l + plot_w}" y2="{margin_t + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>
      <line x1="{margin_l + plot_w}" y1="{margin_t}" x2="{margin_l + plot_w}" y2="{margin_t + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>

      <!-- Left Y Axis Labels (Frequency) -->
      <text x="{margin_l - 10}" y="{margin_t + 5}" font-family="Segoe UI, sans-serif" font-size="10" fill="#475569" text-anchor="end">20</text>
      <text x="{margin_l - 10}" y="{margin_t + plot_h/2}" font-family="Segoe UI, sans-serif" font-size="10" fill="#475569" text-anchor="end">10</text>
      <text x="{margin_l - 10}" y="{margin_t + plot_h}" font-family="Segoe UI, sans-serif" font-size="10" fill="#475569" text-anchor="end">0</text>
      <text x="{margin_l - 30}" y="{margin_t + plot_h/2}" font-family="Segoe UI, sans-serif" font-size="11" font-weight="bold" fill="#1e40af" transform="rotate(-90 {margin_l - 30} {margin_t + plot_h/2})" text-anchor="middle">Defect Frequency (Count)</text>

      <!-- Right Y Axis Labels (Cumulative %) -->
      <text x="{margin_l + plot_w + 10}" y="{margin_t + 5}" font-family="Segoe UI, sans-serif" font-size="10" fill="#475569">100%</text>
      <text x="{margin_l + plot_w + 10}" y="{margin_t + plot_h/2}" font-family="Segoe UI, sans-serif" font-size="10" fill="#475569">50%</text>
      <text x="{margin_l + plot_w + 10}" y="{margin_t + plot_h}" font-family="Segoe UI, sans-serif" font-size="10" fill="#475569">0%</text>

      <!-- Bars -->
      {''.join(bars_svg)}

      <!-- 80% Cutoff Line -->
      {line_80_svg}

      <!-- Cumulative Line -->
      <polyline points="{' '.join(line_points)}" fill="none" stroke="#dc2626" stroke-width="2.5"/>
      {''.join(circles_svg)}

      <!-- Category Labels -->
      {''.join(labels_svg)}
    </svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated Pareto Chart SVG: {output_path}")


def generate_fishbone_svg(output_path="fishbone_diagram.svg"):
    """Generates an Ishikawa (Fishbone) Diagram vector SVG."""
    svg_w, svg_h = 820, 480
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
      <rect width="100%" height="100%" fill="#ffffff" rx="8"/>
      <text x="{svg_w / 2}" y="32" font-family="Segoe UI, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">
        Ishikawa (Fishbone) Root Cause Diagram
      </text>
      <text x="{svg_w / 2}" y="48" font-family="Segoe UI, sans-serif" font-size="11" fill="#64748b" text-anchor="middle">
        Root Causes of Inventory Stockouts & Inaccessibility • Rahul Mehra (CSE AIML Sec B)
      </text>

      <!-- Central Spine -->
      <line x1="60" y1="240" x2="620" y2="240" stroke="#0f172a" stroke-width="4"/>
      <polygon points="620,230 650,240 620,250" fill="#0f172a"/>

      <!-- Problem Head (Effect) -->
      <rect x="650" y="200" width="150" height="80" rx="8" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
      <text x="725" y="235" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#991b1b" text-anchor="middle">INVENTORY</text>
      <text x="725" y="250" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#991b1b" text-anchor="middle">STOCKOUTS &</text>
      <text x="725" y="265" font-family="Segoe UI, sans-serif" font-size="11" font-weight="bold" fill="#991b1b" text-anchor="middle">INACCESSIBILITY</text>

      <!-- TOP BONES: PEOPLE & PROCESS -->
      <!-- Bone 1: People -->
      <line x1="160" y1="90" x2="250" y2="240" stroke="#2563eb" stroke-width="2.5"/>
      <rect x="100" y="65" width="120" height="28" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="160" y="84" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#1e40af" text-anchor="middle">1. PEOPLE</text>
      
      <line x1="130" y1="140" x2="200" y2="155" stroke="#64748b" stroke-width="1.5"/>
      <text x="125" y="138" font-family="Segoe UI, sans-serif" font-size="10" fill="#334155" text-anchor="end">No accessibility training</text>
      
      <line x1="160" y1="180" x2="225" y2="195" stroke="#64748b" stroke-width="1.5"/>
      <text x="155" y="178" font-family="Segoe UI, sans-serif" font-size="10" fill="#334155" text-anchor="end">Manual counting oversight</text>

      <!-- Bone 2: Process -->
      <line x1="390" y1="90" x2="480" y2="240" stroke="#2563eb" stroke-width="2.5"/>
      <rect x="330" y="65" width="120" height="28" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
      <text x="390" y="84" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#1e40af" text-anchor="middle">2. PROCESS</text>

      <line x1="360" y1="140" x2="430" y2="155" stroke="#64748b" stroke-width="1.5"/>
      <text x="355" y="138" font-family="Segoe UI, sans-serif" font-size="10" fill="#334155" text-anchor="end">Delayed reorder triggers</text>

      <line x1="390" y1="180" x2="455" y2="195" stroke="#64748b" stroke-width="1.5"/>
      <text x="385" y="178" font-family="Segoe UI, sans-serif" font-size="10" fill="#334155" text-anchor="end">No safety stock formulas</text>

      <!-- BOTTOM BONES: SOFTWARE CODE & INFRASTRUCTURE -->
      <!-- Bone 3: Software Code -->
      <line x1="160" y1="390" x2="250" y2="240" stroke="#16a34a" stroke-width="2.5"/>
      <rect x="90" y="390" width="140" height="28" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
      <text x="160" y="409" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#15803d" text-anchor="middle">3. SOFTWARE CODE</text>

      <line x1="130" y1="340" x2="200" y2="325" stroke="#64748b" stroke-width="1.5"/>
      <text x="125" y="343" font-family="Segoe UI, sans-serif" font-size="10" fill="#334155" text-anchor="end">Low-contrast CSS palettes</text>

      <line x1="160" y1="300" x2="225" y2="285" stroke="#64748b" stroke-width="1.5"/>
      <text x="155" y="303" font-family="Segoe UI, sans-serif" font-size="10" fill="#334155" text-anchor="end">Missing keyboard tab traps</text>

      <!-- Bone 4: Infrastructure -->
      <line x1="390" y1="390" x2="480" y2="240" stroke="#16a34a" stroke-width="2.5"/>
      <rect x="310" y="390" width="160" height="28" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
      <text x="390" y="409" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#15803d" text-anchor="middle">4. INFRASTRUCTURE</text>

      <line x1="360" y1="340" x2="430" y2="325" stroke="#64748b" stroke-width="1.5"/>
      <text x="355" y="343" font-family="Segoe UI, sans-serif" font-size="10" fill="#334155" text-anchor="end">Poor lab room ambient light</text>

      <line x1="390" y1="300" x2="455" y2="285" stroke="#64748b" stroke-width="1.5"/>
      <text x="385" y="303" font-family="Segoe UI, sans-serif" font-size="10" fill="#334155" text-anchor="end">Disorganized storage racks</text>
    </svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated Fishbone Diagram SVG: {output_path}")

if __name__ == "__main__":
    generate_pareto_svg()
    generate_fishbone_svg()
