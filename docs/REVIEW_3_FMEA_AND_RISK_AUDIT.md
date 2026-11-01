# BBAT104: Fundamentals of Total Quality Management (TQM)
## Review 3: FMEA & Risk Audit Report
**Academic Session:** 2026–27 | **Assessment Weightage:** 15 Raw Marks (Mapped to CO2)

---

### Student & Project Demographics
- **Student Name:** Rahul Mehra
- **Department / Specialization:** Computer Science & Engineering (Artificial Intelligence & Machine Learning)
- **Section:** SEC-B
- **Roll Number Baseline Digit:** **3** (Inventory Management System)
- **Core TQM Goal Application:** *Eliminate stockouts & track turnover rate*
- **Assigned Quality Goal:** **Q12: Improve Accessibility**
- **Evaluation Criteria:** FMEA Matrix with RPN scores, SIPOC Process Map, CTQ Tree, Defect Logging Standards.

---

## 1. SIPOC Process Map (High-Level Process Boundary)

The **SIPOC** framework (Suppliers, Inputs, Process, Outputs, Customers) demarcates the end-to-end laboratory inventory workflow to isolate quality vulnerabilities before they reach student researchers.

```
+-----------------------------------------------------------------------------------------------------------------------+
|                                                  SIPOC PROCESS MAP                                                    |
+---------------------+-------------------+-------------------------------+---------------------+-----------------------+
| SUPPLIERS           | INPUTS            | PROCESS (STEPS)               | OUTPUTS             | CUSTOMERS             |
+---------------------+-------------------+-------------------------------+---------------------+-----------------------+
| • Hardware Vendors  | • Component POs   | 1. Asset Delivery Inspection  | • Verified Physical | • CSE AIML Lab        |
|   (NVIDIA, Intel,   | • Serial Numbers  | 2. Poka-Yoke Data Intake      |   Stock             |   Students            |
|   Element14,        | • Manufacturer    | 3. Dynamic Threshold ROP      | • Immutable SQLite  | • Project Faculty     |
|   Arduino, Robu)    |   Datasheets      |    Calculation                |   Catalog Record    |   Evaluators          |
| • Lab Faculty &     | • Reorder Points  | 4. Student Component Issue    | • Instant Stockout  | • Academic Lab        |
|   Lab Technicians   | • Accessibility   |    with Automatic Logging     |   Warning Badges    |   Technicians         |
| • Department Stores |   User Preferences| 5. On-Demand Accessibility    | • Annual Turnover   | • Dept. Purchase      |
|   Committee         |   (Contrast, Font)|    Reconfiguration (Alt+H)    |   & FSN Reports     |   Committee           |
+---------------------+-------------------+-------------------------------+---------------------+-----------------------+
```

### Detailed Process Steps:
1. **Intake & Verification:** Lab technician inspects physical packaging, checks component pins/connectors, and verifies purchase order specifications.
2. **Data Logging (Poka-Yoke):** User enters SKU, model, category, unit price, and storage location. System prevents submission if required fields are missing or if the SKU already exists.
3. **Safety Stock & ROP Calibration:** Mathematical calculation of Safety Stock ($SS$) and Reorder Point ($ROP$) based on procurement lead time (7 days) and estimated student demand.
4. **Issuance & Tracking:** Components issued to student project groups. System decrements physical count, increments `units_issued`, and logs the timestamp in `audit_logs`.
5. **Quality Review:** Continuous monitoring of stockout risks, FSN turnover status, and interface accessibility audits.

---

## 2. Critical to Quality (CTQ) Tree

The **CTQ Tree** translates qualitative customer needs (Voice of the Customer - VoC) into measurable, verifiable technical specifications.

```
[VOICE OF THE CUSTOMER (NEED)]
"We need a reliable, inclusive lab inventory system where equipment is always in stock
 and the software is operable by everyone, including visually or motor-impaired students."
       │
       ├───► [QUALITY DRIVER 1: RELIABLE HARDWARE AVAILABILITY (DIGIT 3)]
       │        │
       │        ├──► CTQ Metric 1.1: Stockout Incidents = 0.0% during academic semester
       │        ├──► CTQ Metric 1.2: Minimum Safety Stock Buffer >= 5 units maintained
       │        └──► CTQ Metric 1.3: Real-time Reorder Point (ROP) alert within 50ms of Q <= Threshold
       │
       ├───► [QUALITY DRIVER 2: INCLUSIVE ACCESSIBILITY (Q12)]
       │        │
       │        ├──► CTQ Metric 2.1: Text Contrast Ratio >= 7.0:1 (WCAG 2.1 Level AAA)
       │        ├──► CTQ Metric 2.2: Dynamic Font Resizing from 80% to 160% without clipping
       │        ├──► CTQ Metric 2.3: 100% of interactive controls operable via Keyboard
       │        └──► CTQ Metric 2.4: Cognitive Clutter Reduction >= 50% in Minimalist Mode
       │
       └───► [QUALITY DRIVER 3: DATA INTEGRITY & AUDITABILITY]
                │
                ├──► CTQ Metric 3.1: Zero duplicate SKU insertions (100% database constraint)
                └──► CTQ Metric 3.2: 100% of state change events written to immutable audit log
```

---

## 3. Failure Mode and Effects Analysis (FMEA)

### 3.1 Rating Scale Standard (Industry Standard 1 to 10 Scale)
To ensure empirical rigor without fabricating institutional standards, we apply the standard **AIAG / ISO 9001 FMEA 1–10 Rating Scale**:

- **Severity (S):**
  - $1$: Negligible annoyance, zero functional disruption.
  - $4\text{--}6$: Moderate disruption, delay in component issuance, visual fatigue.
  - $7\text{--}8$: Significant failure, system inoperable for disabled users, data corruption risk.
  - $9\text{--}10$: Critical failure, project viva halted, lab safety breach.
- **Occurrence (O):**
  - $1$: Extremely unlikely ($< 1$ in $10,000$ operations).
  - $3\text{--}4$: Low frequency (isolated occurrences).
  - $5\text{--}7$: Moderate frequency (weekly or recurring human errors).
  - $8\text{--}10$: Inevitable / high frequency ($> 1$ in $10$ operations).
- **Detection (D):**
  - $1\text{--}2$: Immediate automatic detection (instant validation error / loud alert).
  - $3\text{--}5$: Detected during normal operational checksheet review.
  - $6\text{--}8$: Hard to detect, discovered only after user complaint.
  - $9\text{--}10$: Undetectable until total system failure occurs.

$$\text{Risk Priority Number } (RPN) = \text{Severity } (S) \times \text{Occurrence } (O) \times \text{Detection } (D)$$

- **Risk Tiers:**
  - $RPN \ge 200$: **High Risk (Critical)** &mdash; Mandatory immediate engineering mitigation.
  - $100 \le RPN < 200$: **Medium Risk** &mdash; Corrective action required.
  - $RPN < 100$: **Low Risk** &mdash; Acceptable baseline operating condition.

---

### 3.2 FMEA Risk Audit Matrix

| ID | Failure Mode | Potential Effect of Failure | Root Cause | S | O | D | **Pre RPN** | Risk Tier | Poka-Yoke / Q12 Mitigation Action | S' | O' | D' | **Post RPN** | % RPN Reduction |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **FM-01** | Lab stockout during final term project exam | Student team cannot execute AI inference testing; academic marks penalized | Reorder request delayed until physical bin reaches 0 units | 9 | 7 | 6 | **378** | **High** | Automatic Reorder Point ($ROP$) calculation + Safety Stock ($SS \ge 5$) buffer trigger | 9 | 2 | 2 | **36** | **90.5%** |
| **FM-02** | Text illegible to student with low vision / astigmatism | Student unable to read hardware specs or inventory tables; visual strain | Fixed low-contrast gray theme with small 10px fonts | 8 | 6 | 7 | **336** | **High** | WCAG AAA High Contrast mode ($\ge 14:1$ ratio) + dynamic font scaler ($80\%\text{--}160\%$) | 8 | 1 | 2 | **16** | **95.2%** |
| **FM-03** | Mouse failure / physical disability prevents data entry | Warehouse or lab assistant unable to save inventory records | Missing keyboard navigation and unmapped hotkeys | 7 | 6 | 6 | **252** | **High** | Full keyboard support: <kbd>Tab</kbd> cycle, focus traps, <kbd>Alt+N</kbd>, <kbd>Alt+S</kbd>, <kbd>Arrows</kbd> | 7 | 1 | 2 | **14** | **94.4%** |
| **FM-04** | Duplicate SKU inserted into catalog | Inventory counts split across two entries; inaccurate auditing | Manual SKU entry without database unique index constraint | 8 | 5 | 5 | **200** | **High** | SQLite `UNIQUE COLLATE NOCASE` index + client-side Poka-Yoke validation check | 8 | 1 | 2 | **16** | **92.0%** |
| **FM-05** | Cognitive sensory overload for neurodivergent/ADHD users | Data entry mistakes and anxiety due to visual clutter and cards | Complex dashboard with multiple metric cards, banners, and badges | 6 | 5 | 5 | **150** | **Medium** | Toggleable Minimalist Layout Mode (<kbd>Alt+M</kbd>) stripping non-essential visual cards | 6 | 2 | 2 | **24** | **84.0%** |
| **FM-06** | Accidental negative stock entry ($Q < 0$) | Distorts inventory valuation and financial audit reports | Lack of input bounds validation | 7 | 4 | 4 | **112** | **Medium** | Database `CHECK (quantity >= 0)` constraint + form type validation | 7 | 1 | 2 | **14** | **87.5%** |
| **FM-07** | Inadvertent component deletion | Permanent loss of historical component records | Single-click delete action without confirmation | 8 | 3 | 4 | **96** | **Low** | Accessible Modal Confirmation Dialog (<kbd>Esc</kbd> to cancel, explicit Enter required) | 8 | 1 | 1 | **8** | **91.7%** |
| **FM-08** | Stagnant/dead stock unnoticed on lab shelves | High capital tied up in unused equipment; budget wasted | Absence of turnover tracking across academic semesters | 6 | 5 | 4 | **120** | **Medium** | Automated Inventory Turnover Ratio ($ITR$) and FSN analysis (Fast, Slow, Non-moving) | 6 | 2 | 2 | **24** | **80.0%** |

---

## 4. Defect Logging Standards & Historical Checksheet

To uphold TQM Principle 6.2 (*Fact-Based Decision Making*), defects encountered during alpha and beta laboratory testing are tracked using a standardized defect log matrix:

```
+---------------------------------------------------------------------------------------------------------+
|                                  STANDARDIZED DEFECT LOG MATRIX                                         |
+---------+--------------------+-------------------------------+----------+------------+------------------+
| LOG ID  | CATEGORY           | DEFECT DESCRIPTION            | SEVERITY | STATUS     | RESOLUTION       |
+---------+--------------------+-------------------------------+----------+------------+------------------+
| DEF-001 | Stockout Alert     | Low-stock alert missed on Q=5 | Critical | Resolved   | Updated ROP rule |
| DEF-002 | Accessibility (Q12)| Dark mode text contrast < 4:1 | High     | Resolved   | Applied #f8fafc  |
| DEF-003 | Keyboard Nav (Q12) | Modal focus escaped on Tab    | High     | Resolved   | Added focus trap |
| DEF-004 | Font Scaling (Q12) | Text truncated at 140% scale  | Medium   | Resolved   | Replaced with rem|
| DEF-005 | Poka-Yoke Input    | Negative stock allowed via API| High     | Resolved   | Added DB CHECK   |
+---------+--------------------+-------------------------------+----------+------------+------------------+
```
*(Complete 50-item defect checksheet analysis is presented in Review 4).*
