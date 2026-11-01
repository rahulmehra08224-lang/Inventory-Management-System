# BBAT104: Fundamentals of Total Quality Management (TQM)
## Review 2: Base System CRUD & Execution of Quality Goal Q12 Features
**Academic Session:** 2026–27 | **Assessment Weightage:** 15 Raw Marks (Mapped to CO1, CO2)

---

### Student & Project Demographics
- **Student Name:** Rahul Mehra
- **Department / Specialization:** Computer Science & Engineering (Artificial Intelligence & Machine Learning)
- **Section:** SEC-B
- **Roll Number Baseline Digit:** **3** (Inventory Management System)
- **Assigned Quality Goal:** **Q12: Improve Accessibility**
- **Quality Features Executed:**
  1. High Contrast Mode
  2. Dynamic Font Resizing Engine
  3. Comprehensive Keyboard Navigation
  4. Dark Mode / Theme Engine
  5. Minimalist Cognitive Layout Mode

---

## 1. Base System CRUD Implementation & Digit 3 TQM Goals

In compliance with the assignment mapping for Digit 3, the base system provides complete **CRUD (Create, Read, Update, Delete)** operations alongside direct algorithmic models for **eliminating stockouts** and **tracking inventory turnover rates**.

### 1.1 Data Model Specification
Each catalog hardware asset stores:
- `id`: Auto-incrementing unique integer primary key.
- `sku`: Unique asset tracking string (e.g., `NV-JET-ORIN-8G`). Enforced unique via database index and client-side pre-validation.
- `name`: Human-readable component name and model.
- `category`: Hardware category (`AI Accelerators`, `Microcontrollers`, `Sensors & Vision`, `Robotics & Actuators`, `Power & Batteries`, `Lab Instruments`).
- `quantity`: Current physical unit count in laboratory stock ($Q \ge 0$).
- `min_threshold`: Safe minimum inventory limit below which reordering is required.
- `unit_price`: Unit asset price in Indian Rupees (₹).
- `units_issued`: Cumulative component issuances for academic lab experiments.
- `supplier`: Authorized lab vendor or academic hardware partner.
- `location`: Shelf, rack, cabinet, or storage bin coordinate.
- `specs`: Key technical and electrical specifications.
- `updated_at`: ISO timestamp of latest inventory movement.

### 1.2 Mathematical Formulations: Stockout Elimination & Turnover

#### A. Stockout Elimination Algorithm
To eliminate laboratory stockouts during student coursework, the system utilizes a **Safety Stock ($SS$)** and **Reorder Point ($ROP$)** model:

$$\text{Safety Stock } (SS) = Z \times \sigma_L = 1.65 \times \sqrt{L \times \sigma_d^2 + d^2 \times \sigma_L^2}$$

Where:
- $Z = 1.65$ represents a **95% Service Level** (statistical Z-score).
- $d = \text{Average daily component usage}$.
- $L = \text{Procurement lead time in days}$.

$$\text{Reorder Point } (ROP) = (d \times L) + SS$$

Whenever physical stock $Q \le ROP$, the system immediately renders an assertive alert (`⚠ LOW STOCK`) and triggers a screen-reader notification.

#### B. Inventory Turnover Ratio & FSN Classification
To detect stale or non-moving capital, the system computes the turnover velocity:

$$\text{Inventory Turnover Ratio } (ITR) = \frac{\text{Annual Units Issued}}{\text{Average Units Held in Stock}}$$

The assets are dynamically categorized into **FSN Analysis**:
- **Fast-Moving (F):** $ITR \ge 2.0\text{x}$ (High student demand, e.g., Jetson Orin, Raspberry Pi 5).
- **Slow-Moving (S):** $0.8\text{x} \le ITR < 2.0\text{x}$ (Moderate project demand).
- **Non-Moving (N):** $ITR < 0.8\text{x}$ (Low circulation, flag for lab reassignment).

---

## 2. Execution of Assigned Quality Goal Features (Q12)

### Feature 1: High Contrast Mode (WCAG AAA Compliance)
- **Objective:** Enable individuals with low vision, photophobia, color vision deficiency, or users under glaring laboratory lighting to clearly distinguish all interface components.
- **Implementation:**
  - Employs stark OLED black (`#000000`) and pure white (`#FFFFFF`) palettes.
  - In High Contrast Dark: Background is `#000000`, primary accent is bright yellow (`#FFE600`), borders are crisp `2px solid #FFFFFF`, and text is pure white.
  - In High Contrast Light: Pure white background, bold black borders (`2px solid #000000`), no subtle grays.
  - Verified text contrast ratio exceeds **14.2:1**, far surpassing the **WCAG 2.1 AAA requirement of 7.0:1**.
  - All interactive elements feature underlined text and high-visibility focus rings.
- **Activation:** Persistent button in toolbar and global hotkey <kbd>Alt + H</kbd>.

### Feature 2: Dynamic Font Resizing Engine
- **Objective:** Allow users with visual impairments or varying screen distances to scale typography without breaking the grid, truncating text, or requiring browser page zoom.
- **Implementation:**
  - Built entirely on CSS Custom Properties (`--font-scale`) bound to responsive `rem` units:
    ```css
    :root {
      --font-scale: 1;
      --fs-base: calc(1rem * var(--font-scale));
      --fs-md: calc(1.125rem * var(--font-scale));
      --fs-xl: calc(1.5rem * var(--font-scale));
    }
    ```
  - Incremental scaling steps: `85%`, `100%`, `125%`, `150%`, and `175%`.
  - Accessible step buttons (<kbd>A-</kbd> and <kbd>A+</kbd>) and reset control.
  - Automatic screen reader announcement of new font scale via `aria-live="polite"`.
- **Activation:** Toolbar controls and keyboard hotkeys <kbd>Alt + +</kbd>, <kbd>Alt + -</kbd>, and <kbd>Alt + 0</kbd>.

### Feature 3: Comprehensive Keyboard Navigation
- **Objective:** Guarantee full application operability for users who cannot use a mouse, motorized wheelchair joystick users, or keyboard power users (WCAG 2.1 Principle 2: Operable).
- **Implementation:**
  - **Skip to Main Content:** First focusable element upon pressing <kbd>Tab</kbd>, bypassing headers.
  - **Visible Focus Rings:** Highly visible 3px outline with 2px offset (`:focus-visible`).
  - **Modal Focus Trapping:** When Add/Edit dialog opens, focus is constrained within the modal; pressing <kbd>Tab</kbd> on the last element cycles to the first. Pressing <kbd>Esc</kbd> closes the modal and returns focus to the initiating button.
  - **Table Arrow Navigation:** Arrow keys (<kbd>&uarr;</kbd> / <kbd>&darr;</kbd>) traverse table rows with live announcements. Pressing <kbd>Enter</kbd> opens the item edit modal.
  - **Global Hotkeys:**
    - <kbd>Alt + N</kbd>: Add New Item
    - <kbd>Alt + S</kbd>: Focus Search Field
    - <kbd>Alt + H</kbd>: Toggle High Contrast
    - <kbd>Alt + D</kbd>: Toggle Dark Theme
    - <kbd>Alt + M</kbd>: Toggle Minimalist View
    - <kbd>Alt + E</kbd>: Export to CSV
    - <kbd>?</kbd>: Open Keyboard Shortcuts Cheat Sheet

### Feature 4: Dark Mode / Theme Engine
- **Objective:** Mitigate digital visual fatigue, reduce blue light exposure, and minimize glare during evening laboratory sessions.
- **Implementation:**
  - Slate dark theme palette (`#0b1120`, `#1e293b`) with balanced muted text (`#94a3b8`) and crisp foreground text (`#f8fafc`).
  - Works orthogonally with High Contrast mode: User can toggle between Standard Light, Standard Dark, High Contrast Light, and High Contrast Dark.
  - State persisted across browser sessions via `localStorage` or SQLite configuration.
- **Activation:** Toolbar toggle button and hotkey <kbd>Alt + D</kbd>.

### Feature 5: Minimalist Cognitive Layout Mode
- **Objective:** Cater to neurodivergent users, students with ADHD, visual sensory overload sensitivities, or users operating under high-magnification screen lenses.
- **Implementation:**
  - Reduces sensory clutter by hiding decorative widgets:
    - Metric overview cards (`.dashboard-metrics`) are hidden.
    - Non-essential badges, decorative icons, and activity streams are hidden.
    - Table borders and padding are streamlined into clean, high-legibility tabular rows.
    - Animation transitions are suppressed.
  - Renders a prominent status banner confirming Minimalist Mode is active with a 1-click restore link.
- **Activation:** Toolbar toggle and hotkey <kbd>Alt + M</kbd>.

---

## 3. Poka-Yoke (Mistake-Proofing) Error Prevention Mechanisms

In accordance with TQM Principle 6.2 (Error Prevention at Entry Level):
1. **Duplicate SKU Prevention:** The system checks SKU uniqueness before database commit. If a duplicate is entered, the field is highlighted in red, an error banner is presented, and focus is shifted directly to the invalid input.
2. **Negative Quantity Lockout:** Form validation forbids values $< 0$ for quantity and $< 1$ for minimum threshold.
3. **Color-Independent Status Indicators:** Status badges combine color with distinct geometric iconography (`✓ In Stock`, `⚠ Low Stock`, `× Out of Stock`), adhering to **WCAG 1.4.1 (Use of Color)** so color is never the single differentiator.
4. **Delete Confirmation Dialog:** Destructive deletion requires explicit verification in an accessible `alertdialog` modal.
