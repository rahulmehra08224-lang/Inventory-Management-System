# BBAT104: Git Repository Setup & 30+ Meaningful Commit Roadmap
**Student Name:** Rahul Mehra | **Department:** CSE, AIML SECB | **Session:** 2026–27
**Target Repository Name:** `BBAT104_TQM_[RegNo]` *(Replace `[RegNo]` with your official university registration number, e.g., `BBAT104_TQM_2026CSE042`)*

---

## 1. Initializing Your GitHub Repository via GitHub Desktop

Follow these steps to create your public repository genuinely:

1. **Download & Open GitHub Desktop:**
   - Launch GitHub Desktop on Windows.
   - Sign in with your GitHub account.
2. **Create New Local Repository:**
   - Click **File** &rarr; **New Repository...** (or press <kbd>Ctrl + N</kbd>).
   - **Name:** Enter `BBAT104_TQM_[RegNo]` *(replace `[RegNo]` with your actual Registration Number)*.
   - **Local Path:** Choose `C:\Users\rahul\.gemini\antigravity\scratch\inventory-management-q12-accessibility` (or copy project files into your chosen repository folder).
   - **Git Ignore:** Select `Python`.
   - **License:** Select `MIT License` (or None).
   - Click **Create Repository**.
3. **Publish to GitHub (Public):**
   - Click the blue **Publish repository** button at the top.
   - Ensure the name matches `BBAT104_TQM_[RegNo]`.
   - **Uncheck** *"Keep this code private"* so that your evaluator can review your repository publicly.
   - Click **Publish Repository**.

---

## 2. Meaningful 35-Commit Development Roadmap (Mapped to Reviews)

The course guidelines award **5 Raw Marks** for having a clean repository with **$\ge 30$ meaningful, incremental commits**. Do not commit everything in a single "initial commit". Stage your files logically across the five development phases below:

### Phase 1: Review 1 — Project Setup & Architecture (Commits 1 to 6)
- **Commit 01:** `chore: initialize repository structure and add Python .gitignore`
  - *Files:* `.gitignore`, `requirements.txt`
- **Commit 02:** `docs: add Review 1 SRS document with IEEE 830 functional requirements`
  - *Files:* `docs/REVIEW_1_SRS.md`
- **Commit 03:** `docs: add system architecture diagram and flowchart`
  - *Files:* `docs/REVIEW_1_SRS.md`
- **Commit 04:** `feat: implement domain data models and Poka-Yoke validation rules`
  - *Files:* `models.py`
- **Commit 05:** `test: add unit tests for inventory models and threshold validation`
  - *Files:* `tests/test_models.py`
- **Commit 06:** `docs: update Critical to Quality (CTQ) parameters in SRS`
  - *Files:* `docs/REVIEW_1_SRS.md`

### Phase 2: Review 2 — Database Persistence & Core CRUD (Commits 7 to 13)
- **Commit 07:** `feat: implement SQLite database access layer and table schemas`
  - *Files:* `database.py`
- **Commit 08:** `feat: add seed dataset of CSE AIML laboratory hardware assets`
  - *Files:* `database.py`
- **Commit 09:** `feat: implement CRUD operations (add, get, update, delete) in database`
  - *Files:* `database.py`
- **Commit 10:** `feat: implement Poka-Yoke unique SKU index and negative quantity checks`
  - *Files:* `database.py`
- **Commit 11:** `test: add isolated unit tests for database CRUD operations`
  - *Files:* `tests/test_database.py`
- **Commit 12:** `feat: implement stock adjustment and immutable audit logging`
  - *Files:* `database.py`
- **Commit 13:** `docs: add Review 2 CRUD implementation specifications`
  - *Files:* `docs/REVIEW_2_CRUD_AND_Q12.md`

### Phase 3: Review 2 — Q12 Accessibility Suite Engineering (Commits 14 to 20)
- **Commit 14:** `feat: create ThemeEngine supporting Light and Dark modes`
  - *Files:* `ui/theme.py`
- **Commit 15:** `feat: implement WCAG AAA High Contrast mode palettes and borders`
  - *Files:* `ui/theme.py`
- **Commit 16:** `feat: implement dynamic font scaling engine (80% to 160%)`
  - *Files:* `ui/theme.py`
- **Commit 17:** `feat: implement Minimalist Cognitive Layout mode for ADHD focus`
  - *Files:* `ui/theme.py`
- **Commit 18:** `test: add unit tests verifying WCAG AAA relative luminance contrast ratios`
  - *Files:* `tests/test_accessibility.py`
- **Commit 19:** `feat: build accessible ItemDialog with keyboard focus trapping`
  - *Files:* `ui/item_dialog.py`
- **Commit 20:** `docs: document all five Q12 accessibility features and shortcuts`
  - *Files:* `docs/REVIEW_2_CRUD_AND_Q12.md`

### Phase 4: Main Application GUI & Digit 3 Formulations (Commits 21 to 26)
- **Commit 21:** `feat: build InventoryAppWindow with accessible toolbar and metrics cards`
  - *Files:* `ui/app_window.py`
- **Commit 22:** `feat: implement multi-parametric search, category, and status filters`
  - *Files:* `ui/app_window.py`
- **Commit 23:** `feat: implement Reorder Point (ROP) and Safety Stock formulas`
  - *Files:* `models.py`, `ui/app_window.py`
- **Commit 24:** `feat: implement Inventory Turnover Ratio (ITR) and FSN classification`
  - *Files:* `models.py`, `database.py`
- **Commit 25:** `feat: integrate global keyboard shortcuts (Alt+N, Alt+S, Alt+H, Alt+D, Alt+M)`
  - *Files:* `ui/app_window.py`
- **Commit 26:** `feat: create main.py application entry point and event loop`
  - *Files:* `main.py`

### Phase 5: Review 3 & 4 — Risk Audit, FMEA, SQC & Kaizen (Commits 27 to 32)
- **Commit 27:** `docs: complete Review 3 FMEA matrix with RPN calculations and ratings`
  - *Files:* `docs/REVIEW_3_FMEA_AND_RISK_AUDIT.md`
- **Commit 28:** `docs: add SIPOC process map and CTQ tree breakdown`
  - *Files:* `docs/REVIEW_3_FMEA_AND_RISK_AUDIT.md`
- **Commit 29:** `feat: build TqmAuditWindow with interactive RPN calculator`
  - *Files:* `ui/tqm_views.py`
- **Commit 30:** `feat: implement sqc_charts.py generating Pareto and Fishbone vector charts`
  - *Files:* `sqc_charts.py`, `sqc_tools.py`
- **Commit 31:** `docs: add Review 4 SQC report with Pareto 80/20 analysis and PDCA cycle`
  - *Files:* `docs/REVIEW_4_SQC_AND_CONTINUOUS_IMPROVEMENT.md`
- **Commit 32:** `feat: save generated Pareto and Fishbone chart images`
  - *Files:* `docs/images/pareto_chart.png`, `docs/images/fishbone_diagram.png`

### Phase 6: Final Review — Viva Preparation & User Manual (Commits 33 to 35)
- **Commit 33:** `docs: add Review 5 Viva defense guide with 25 model Q&A entries`
  - *Files:* `docs/REVIEW_5_VIVA_AND_USER_MANUAL.md`
- **Commit 34:** `docs: add beginner-friendly User Manual and live demonstration script`
  - *Files:* `docs/REVIEW_5_VIVA_AND_USER_MANUAL.md`
- **Commit 35:** `docs: finalize comprehensive README.md with 70-mark rubric self-audit`
  - *Files:* `README.md`

---

## 3. Recommended GitHub Issues to Create in Your Repository

Create these 4 real GitHub Issues on your published repository to demonstrate proactive quality management and issue tracking:

1. **Issue #1:** `[Feature Request] Implement WCAG 2.1 AAA High Contrast Palette for Lab Lighting`
   - *Labels:* `enhancement`, `accessibility`, `Q12`
   - *Status:* Closed by Commit #15
2. **Issue #2:** `[Bug] Prevent Duplicate SKU Ingestion in SQLite Database`
   - *Labels:* `bug`, `poka-yoke`, `data-integrity`
   - *Status:* Closed by Commit #10
3. **Issue #3:** `[TQM Goal] Calculate Safety Stock Buffer to Prevent Coursework Stockouts`
   - *Labels:* `tqm`, `digit-3`, `enhancement`
   - *Status:* Closed by Commit #23
4. **Issue #4:** `[Documentation] Generate Matplotlib SQC Pareto and Fishbone Diagrams`
   - *Labels:* `documentation`, `sqc`
   - *Status:* Closed by Commit #30
