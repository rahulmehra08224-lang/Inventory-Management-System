# BBAT104: Fundamentals of Total Quality Management (TQM)
## Review 5 & 6: Viva Defense Guide, Demonstration Sequence & User Manual
**Academic Session:** 2026–27 | **Assessment Weightage:** 15 Raw Marks (10 Viva Marks + 5 Documentation Marks)

---

### Student & Project Demographics
- **Student Name:** Rahul Mehra
- **Department / Specialization:** Computer Science & Engineering (Artificial Intelligence & Machine Learning)
- **Section:** SEC-B
- **Roll Number Baseline Digit:** **3** (Inventory Management System)
- **Core TQM Goal Application:** *Eliminate stockouts & track turnover rate*
- **Assigned Quality Goal:** **Q12: Improve Accessibility**

---

## 1. Live Software Demonstration Script (Step-by-Step for Evaluator)

When presenting your 5-minute live software defense, execute this exact sequence to demonstrate full compliance with both **Digit 3** and **Q12**:

### Step 1: System Launch & Architecture Overview (45 Seconds)
1. Open PowerShell or Terminal in the project root:
   ```powershell
   python main.py
   ```
2. State to the evaluator:
   > *"Good morning/afternoon, Sir/Ma'am. My name is Rahul Mehra, CSE AIML Section B. My assigned baseline is Digit 3: Inventory Management System with the TQM goal of eliminating stockouts and tracking turnover. My assigned quality goal is Q12: Improve Accessibility with all five required features: High Contrast, Font Resizing, Keyboard Navigation, Dark Mode, and Minimalist Layout. The primary desktop application is built in Python 3.x using Tkinter and SQLite3, backed by a 24-test automated test suite and Matplotlib SQC charts."*

### Step 2: Demonstrating the 5 Accessibility Features (Q12) (90 Seconds)
1. **Dynamic Font Resizing:**
   - Press <kbd>Alt + +</kbd> twice. Point to the toolbar: font scale increases to 120% and 140%.
   - Show how the entire table row height, headings, and metric cards scale proportionately without any text truncation.
   - Press <kbd>Alt + 0</kbd> to return smoothly to 100%.
2. **High Contrast Mode (WCAG AAA):**
   - Press <kbd>Alt + H</kbd>. Point out the stark pure white background, bold 2px black borders, and zero gray text (achieving 21:1 contrast ratio).
   - Press <kbd>Alt + D</kbd> while High Contrast is enabled. The theme shifts to OLED black (`#000000`), vivid yellow (`#FFE600`), and pure white, designed for low-vision and astigmatism accommodations.
3. **Dark Mode:**
   - Press <kbd>Alt + H</kbd> to return to standard contrast, keeping Dark Mode active. Point out the eye-friendly slate dark palette (`#0b1120`, `#1e293b`).
4. **Minimalist Cognitive Layout:**
   - Press <kbd>Alt + M</kbd>. Demonstrate how all decorative dashboard cards and subtitle banners instantly disappear, leaving a distilled, high-focus data table. Explain that this satisfies cognitive accessibility for ADHD or neurodivergent users.
   - Press <kbd>Alt + M</kbd> again to restore the full view.
5. **Keyboard Navigation & Hotkeys:**
   - Put your hands in plain view away from the mouse!
   - Press <kbd>Alt + S</kbd> &rarr; search bar is focused immediately. Type `Jetson`. The table dynamically filters to the NVIDIA Jetson Orin.
   - Press <kbd>Esc</kbd> &rarr; search query clears.
   - Use <kbd>&uarr;</kbd> and <kbd>&darr;</kbd> arrow keys to navigate table rows. Press <kbd>Enter</kbd> on a selected row to open the accessible Edit dialog. Press <kbd>Esc</kbd> to dismiss the modal.

### Step 3: Demonstrating Baseline Digit 3 & CRUD Operations (90 Seconds)
1. **Poka-Yoke Add Item:**
   - Press <kbd>Alt + N</kbd>. The Add Asset dialog opens.
   - Leave SKU blank and click Save &rarr; immediate validation alert appears (*"SKU / Asset Code is mandatory"*).
   - Enter duplicate SKU `NV-JET-ORIN-8G` &rarr; system prevents insertion (*"SKU already exists in catalog"*).
   - Enter a new unique item: SKU `ESP32-CAM-01`, Name `ESP32 Camera Module`, Category `Sensors & Vision`, Qty `15`, Threshold `5`, Price `650.00`. Save item.
   - Show that the item appears immediately in the table and updates the dashboard statistics.
2. **Stockout Elimination & Quick Adjustments:**
   - Select the newly added item and click `Decrement Stock` repeatedly until quantity drops to 5.
   - Show how the status badge changes immediately to `⚠ Low Stock (5/5)`.
   - Decrement further to 0 &rarr; badge updates to `× Out of Stock`.
   - Explain the Reorder Point formula: $ROP = (d \times L) + SS$.
3. **Turnover Tracking (FSN Analysis):**
   - Point to the `Turnover (FSN)` column in the table. Show how fast-moving parts (e.g. Jetson Orin with ratio 2.6x) are labeled `Fast (F)`, whereas low-circulation parts are tagged `Non-Moving (N)`.

### Step 4: Demonstrating TQM & SQC Audit Suite (60 Seconds)
1. Click the `📊 TQM & SQC Audit` button on the top right.
2. Walk through the tabs:
   - **Tab 1:** FMEA Risk Audit with the interactive RPN calculator. Change Severity from 9 to 9, Occurrence from 7 to 2, Detection from 6 to 2 &rarr; watch RPN drop from 378 down to 36 (90.5% risk reduction)!
   - **Tab 2:** SIPOC process map and CTQ tree.
   - **Tab 3:** Pareto 80/20 analysis (showing how the top 3 causes drive 78% of defects) and Ishikawa Fishbone root cause diagram.
   - **Tab 4:** Plan-Do-Check-Act (PDCA) Kaizen improvement log.

### Step 5: Demonstrating Data Portability & Tests (15 Seconds)
1. Click `Export CSV (Alt+E)` to export the live catalog.
2. Run automated tests in terminal:
   ```powershell
   python -m unittest discover tests
   ```
   Show all 24 tests passing with 0 errors!

---

## 2. Comprehensive Viva Voce Defense Guide (25 Questions & Model Answers)

### Category A: Total Quality Management (TQM) Principles

#### Q1: What is Total Quality Management (TQM), and how is it applied in your software project?
**Answer:**
TQM is a management philosophy focused on continuous, organization-wide improvement in product quality, customer satisfaction, and process integrity. In this software project, TQM is applied through:
1. **Customer Focus:** Designing features around user needs (preventing stockouts for students and providing accessible UI for impaired users).
2. **Process-Centricity:** Mapping data intake and component issuance via a SIPOC diagram.
3. **Error Prevention (Poka-Yoke):** Using database unique indexes and form masks to prevent invalid or duplicate data at the point of entry.
4. **Fact-Based Decision Making:** Using empirical defect checksheets and Pareto analysis to prioritize engineering fixes.
5. **Continuous Improvement (Kaizen):** Iterating through Plan-Do-Check-Act (PDCA) cycles to raise accessibility from failing to WCAG AAA.

#### Q2: What is Poka-Yoke, and where is it implemented in your code?
**Answer:**
*Poka-Yoke* is a Japanese term meaning "mistake-proofing" or "inadvertent error prevention." In our codebase:
- In `models.py` (`InventoryItem.validate()`): Checks that SKU is between 3–30 characters, quantity $\ge 0$, threshold $\ge 1$, and price $\ge 0$ before execution.
- In `database.py`: Enforces SQLite `UNIQUE COLLATE NOCASE` on the SKU column and `CHECK (quantity >= 0)`.
- In `ui/item_dialog.py`: Highlights invalid fields in red with descriptive inline error labels, preventing bad data from entering the database.

#### Q3: What is the difference between Quality Control (QC) and Quality Assurance (QA)?
**Answer:**
- **Quality Assurance (QA)** is process-oriented and proactive; it focuses on defect *prevention* (e.g. creating coding standards, SRS documents, FMEA risk assessments, and Poka-Yoke validation rules).
- **Quality Control (QC)** is product-oriented and reactive; it focuses on defect *identification* (e.g. running our 24 automated unit tests in `tests/`, verifying contrast ratios, and conducting defect logging).

---

### Category B: Baseline Digit 3 (Stockouts & Turnover)

#### Q4: Why is eliminating stockouts critical, and what mathematical model did you use?
**Answer:**
Stockouts disrupt academic project deadlines and halt AI inference experiments. We eliminated stockouts using a statistical **Safety Stock ($SS$)** and **Reorder Point ($ROP$)** model:
$$SS = Z \times \sigma_L = 1.65 \times \sqrt{L \times \sigma_d^2}$$
For a 95% service level ($Z = 1.65$) with lead time $L = 7$ days and daily demand variation, the safety buffer is calculated at $\approx 5$ units. The Reorder Point is:
$$ROP = (\text{Daily Usage} \times \text{Lead Time}) + SS$$
When physical stock drops to or below the $ROP$, the system flags the item as `⚠ Low Stock` to trigger replenishment before zero balance.

#### Q5: What is the Inventory Turnover Ratio (ITR), and how does FSN Analysis work?
**Answer:**
The Inventory Turnover Ratio measures capital velocity &mdash; how many times inventory is utilized and replaced over a time period:
$$ITR = \frac{\text{Units Issued to Students}}{\max(1, \text{Current Stock Held})}$$
Based on this ratio, we execute **FSN Classification**:
- **Fast-Moving (F):** $ITR \ge 2.0\text{x}$ (high academic demand, e.g., Jetson Orin, Raspberry Pi 5).
- **Slow-Moving (S):** $0.8\text{x} \le ITR < 2.0\text{x}$ (moderate utilization).
- **Non-Moving (N):** $ITR < 0.8\text{x}$ (stagnant inventory flagged for curriculum reallocation).

---

### Category C: Quality Goal Q12 (Accessibility)

#### Q6: Explain your implementation of High Contrast Mode and its WCAG compliance.
**Answer:**
High Contrast mode is designed for users with low vision, astigmatism, or operating under glaring lab lighting. It implements two high-contrast palettes:
1. **Light High Contrast:** Pure black text (`#000000`) on pure white (`#FFFFFF`) with 2px solid black borders and zero gray text.
2. **Dark High Contrast:** Pure OLED black (`#000000`), stark bright yellow (`#FFE600`) for accents, and pure white for text.
Using the WCAG 2.1 relative luminance equation, our contrast ratio is **21.0:1** for black-on-white and **17.5:1** for yellow-on-black, substantially surpassing the **WCAG 2.1 Level AAA requirement of 7.0:1**.

#### Q7: How does your dynamic font resizing engine work without breaking UI layouts?
**Answer:**
In `ui/theme.py`, typography is controlled via a centralized scaling multiplier `font_scale` (ranging from 0.80x to 1.60x in discrete 20% steps). All fonts in labels, headings, inputs, and Treeview rows derive their point size dynamically from:
$$\text{Scaled Size} = \max(8, \text{int}(\text{Base Size} \times \text{font\_scale}))$$
Treeview row heights adapt dynamically (`rowheight = 26 * font_scale`), preventing text clipping or overflow.

#### Q8: How did you ensure 100% Keyboard Navigation operability?
**Answer:**
Following **WCAG 2.1 Principle 2 (Operable)**:
1. Every interactive control is reachable via logical <kbd>Tab</kbd> order.
2. In modal dialogs (`ui/item_dialog.py`), focus is trapped inside the window, cycling between inputs and action buttons.
3. High-visibility focus indicators highlight active inputs.
4. Hotkeys are provided for every major workflow: <kbd>Alt+N</kbd> (New), <kbd>Alt+S</kbd> (Search), <kbd>Alt+H</kbd> (High Contrast), <kbd>Alt+D</kbd> (Dark Theme), <kbd>Alt+M</kbd> (Minimalist), <kbd>Arrows</kbd> (Row navigation), <kbd>Enter</kbd> (Edit), <kbd>Del</kbd> (Delete), and <kbd>Esc</kbd> (Dismiss).

#### Q9: What is the purpose of the Minimalist Layout Mode from an accessibility perspective?
**Answer:**
Minimalist mode addresses **cognitive accessibility** for neurodivergent individuals, users with ADHD, or those experiencing visual sensory overload. When activated (<kbd>Alt+M</kbd>), the application hides decorative metric cards, secondary subtitle banners, and non-essential badges, leaving a clean, stark tabular view that minimizes cognitive friction during repetitive stock entry.

---

### Category D: Statistical Quality Control (SQC) Tools & Risk Analysis

#### Q10: What is FMEA, and how is the Risk Priority Number (RPN) calculated?
**Answer:**
Failure Mode and Effects Analysis (FMEA) is a systematic method for identifying potential process or software design failures before they happen. The Risk Priority Number is calculated as:
$$RPN = \text{Severity } (S) \times \text{Occurrence } (O) \times \text{Detection } (D)$$
Each factor is rated on an industry-standard 1 to 10 scale. In our project, the highest initial risk was **FM-01 (Lab Stockout during project exams)** with $S=9, O=7, D=6 \implies RPN = 378$. After implementing automated safety stock buffers and ROP alerts, the score dropped to $S=9, O=2, D=2 \implies RPN = 36$, representing a **90.5% risk reduction**.

#### Q11: Explain your Pareto Analysis findings.
**Answer:**
Using our 50-item defect audit checksheet, we ranked failure categories by frequency. The Pareto 80/20 rule revealed that the top three defect categories &mdash; **Unnotified Stockouts (36%)**, **Low Contrast Inaccessibility (24%)**, and **Manual Count Drift (18%)** &mdash; accounted for **78.0% of all recorded defects**. By focusing our engineering efforts on these "Vital Few," we resolved ~80% of system vulnerabilities.

#### Q12: Explain the four categories in your Ishikawa (Fishbone) Diagram.
**Answer:**
We structured the root causes of *Inventory Stockouts & Inaccessibility* across the **4P framework**:
1. **People:** Lack of accessibility training and manual counting fatigue.
2. **Process:** Reactive reordering only after stock reaches zero, and absence of statistical safety buffers.
3. **Software Code:** Fixed 10px fonts, low-contrast palettes, and missing focus traps.
4. **Environment:** Harsh laboratory lighting causing screen glare and disorganized physical shelves.

#### Q13: What is the PDCA Cycle, and how did you use it?
**Answer:**
PDCA stands for **Plan-Do-Check-Act**, the foundational cycle of continuous improvement (*Kaizen*):
- **Plan:** Identify baseline weaknesses (e.g. contrast ratio failing at 2.4:1; stockouts occurring 18 times).
- **Do:** Program solutions (ThemeEngine high-contrast palettes, safety stock equations, focus traps).
- **Check:** Measure results against CTQ targets (verified 21:1 contrast ratio, 0 stockouts in 50 test cycles, 24 unit tests passing).
- **Act:** Standardize configurations in `v2.0` release and automate SQC chart generation.

---

### Category E: Software Architecture, Database & Testing

#### Q14: Why did you choose SQLite3, and how is data integrity guaranteed?
**Answer:**
SQLite3 is an embedded, ACID-compliant relational database engine included with standard Python. It requires zero server setup, making it lightweight and reliable for local laboratory deployment. Integrity is guaranteed through:
- Primary key auto-increment constraints.
- `UNIQUE COLLATE NOCASE` on the SKU code to prevent case-sensitive duplicates.
- `CHECK (quantity >= 0)` and `CHECK (min_threshold >= 1)` to prevent negative inventories.
- Atomic transactions (`conn.commit()`) wrapped in Python context managers.

#### Q15: What automated tests did you write, and what did they verify?
**Answer:**
We developed a 24-test unit test suite in `tests/`:
1. `test_models.py` (8 tests): Verifies model validation, boundary rejection, stock status flags (`IN_STOCK`, `LOW_STOCK`, `OUT_OF_STOCK`), turnover ratio calculation, and FSN classification.
2. `test_database.py` (9 tests): Verifies SQLite initialization, CRUD transactions, duplicate SKU rejection, stock increment/decrement clamping, multi-field search, filtering, and audit log persistence using temporary isolated databases.
3. `test_accessibility.py` (7 tests): Verifies font scaling step bounds (0.80x to 1.60x), theme toggling, and mathematically verifies WCAG AAA contrast ratios using relative luminance equations.

#### Q16: What are the honest limitations of your current system?
**Answer:**
1. **Single-User Local Deployment:** SQLite is optimized for local workstation access; multi-station concurrent network writes would benefit from PostgreSQL or MySQL in enterprise production.
2. **Barcode Scanner Hardware Integration:** Data intake currently relies on keyboard/USB input; direct hardware integration with handheld 2D barcode/RFID scanners is planned for future versions.
3. **Automated Supplier API Purchase Orders:** The system currently alerts lab staff and exports CSV/JSON files, rather than firing automated EDI purchase orders directly to vendor ERP systems.

---

## 3. Beginner-Friendly User Manual

### 3.1 System Requirements & Launch Instructions
- **Operating System:** Windows 10 / 11, macOS, or Linux.
- **Python Version:** Python 3.8 or higher.
- **Dependencies:** Standard library (`tkinter`, `sqlite3`). Optional: `matplotlib` (for SQC charts).
- **Launch Command:**
  ```powershell
  python main.py
  ```

### 3.2 Common Operational Tasks

#### How to Add a New Hardware Asset:
1. Click **+ Add New Item** or press <kbd>Alt + N</kbd>.
2. Fill in the required fields: SKU Code, Item Name, Category, Stock Quantity, Alert Threshold, and Unit Price.
3. Press <kbd>Enter</kbd> or click **Save Asset Details**.

#### How to Adjust Stock Quickly:
1. Click any row in the table or navigate using <kbd>&uarr;</kbd> / <kbd>&darr;</kbd> arrow keys.
2. Click **+ Increment Stock** to add 1 unit, or **- Decrement Stock** to deduct 1 unit.
3. The dashboard valuation, stock status badge, and turnover ratios update immediately.

#### How to Toggle High Contrast Mode:
- Click **High Contrast** in the top toolbar or press <kbd>Alt + H</kbd>.
- To switch to Dark High Contrast, press <kbd>Alt + D</kbd> while High Contrast is active.

#### How to Scale Typography:
- Click **A+** or press <kbd>Alt + +</kbd> to increase font size.
- Click **A-** or press <kbd>Alt + -</kbd> to decrease font size.
- Press <kbd>Alt + 0</kbd> to restore standard 100% scaling.

#### How to Export Catalog Data:
- Click **Export CSV** or press <kbd>Alt + E</kbd> to save a UTF-8 spreadsheet of all assets.
- Click **Export JSON** to save structured machine-readable catalog data.
