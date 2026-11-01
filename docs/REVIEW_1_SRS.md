# BBAT104: Fundamentals of Total Quality Management (TQM)
## Review 1: Project Setup, System Architecture & SRS Document
**Academic Session:** 2026–27 | **Assessment Weightage:** 10 Raw Marks (Mapped to CO1)

---

### Student & Project Demographics
- **Student Name:** Rahul Mehra
- **Branch / Specialization:** Computer Science & Engineering (Artificial Intelligence & Machine Learning)
- **Section:** SEC-B
- **Roll Number Assignment Rule:** Digit ending in **3**
- **Assigned Baseline System:** **Inventory Management System**
- **Core TQM Goal Application:** *Eliminate stockouts & track turnover rate*
- **Assigned Sequential Quality Goal:** **Q12: Improve Accessibility**
- **Mandatory Quality Features (Any 5):** 
  1. High Contrast Mode (WCAG AAA)
  2. Dynamic Font Resizing Engine
  3. Comprehensive Keyboard Navigation & Shortcuts
  4. Dark / Light Theme Engine
  5. Minimalist Cognitive Layout Mode

---

## 1. Project Scope & Executive Objectives

The **CSE AIML Hardware Inventory Management System** is engineered to eliminate laboratory component stockouts, monitor stock turnover ratios, and guarantee 100% universal digital accessibility for students and researchers.

### 1.1 Scope Boundaries
- **In-Scope:**
  - Automated tracking of CSE AIML laboratory assets (Edge TPUs, Jetson Dev Kits, Microcontrollers, Depth Cameras, Sensors, Robotics Actuators).
  - Real-time stockout risk alerts based on Safety Stock ($SS$) and Reorder Point ($ROP$) thresholds.
  - Calculation of Inventory Turnover Ratios and Fast-Slow-Non-moving (FSN) inventory classification.
  - Implementation of all 5 features under Quality Goal Q12 meeting WCAG 2.1 AA/AAA compliance.
  - Statistical Quality Control (SQC) audit trail, FMEA risk mitigation, and continuous PDCA improvement.
- **Out-of-Scope:**
  - External banking gateway integration (handled via institutional internal PO voucher system).
  - Inter-campus courier dispatch logistics.

---

## 2. System Architecture Flowchart

```
+-----------------------------------------------------------------------------------+
|                           USER INTERACTION LAYER                                  |
|  [Keyboard Only (Tab/Arrows/Hotkeys)]  <-->  [Mouse / Touch / Screen Reader]      |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        Q12 ACCESSIBILITY CONTROLLER                               |
|  • Font Resizing Engine (85% to 175% rem scaling)                                 |
|  • Contrast Switcher (Normal Contrast <-> WCAG AAA OLED High Contrast)            |
|  • Theme Manager (Slate Dark Mode <-> Clean Light Mode)                           |
|  • Cognitive Filter (Minimalist Distraction-Free Layout vs Standard Full View)   |
|  • ARIA Live Announcer & Keyboard Focus Trap Manager                              |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        CORE INVENTORY APPLICATION LOGIC                           |
|  • Dynamic Search & Multi-Parametric Filter (Category, Stock Level, Specs)        |
|  • Stock Adjustment Engine (+/- count, Instant Recalculation)                     |
|  • Stockout Prevention Algorithm (Safety Stock SS & Reorder Point ROP)            |
|  • Turnover Analytics & FSN Classification Engine (Fast / Slow / Non-moving)      |
|  • Poka-Yoke Input Validation (Unique SKU check, Boundary restrictions)           |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                         DATA PERSISTENCE & AUDIT LAYER                            |
|  • SQLite3 Database (inventory.db) / Browser LocalStorage Engine                  |
|  • Automated Activity & Audit Log Matrix (Timestamped change events)              |
|  • CSV / JSON Structured Data Export & Import Handler                             |
+-----------------------------------------------------------------------------------+
```

---

## 3. Software Requirements Specification (SRS) - IEEE 830 Standard

### 3.1 Functional Requirements (FR)

| Req ID | Module | Functional Description | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | Item CRUD | User can add, view, edit, and delete hardware items with unique SKU, name, category, quantity, threshold, unit price, supplier, location, and specs. | High |
| **FR-02** | Stockout Prevention | System triggers visual and screen-reader alerts whenever quantity drops to or below the minimum alert threshold ($Qty \le Threshold$). | Critical |
| **FR-03** | Turnover Tracking | System computes Inventory Turnover Ratio: $Turnover = \frac{\text{Units Issued}}{\max(1, \text{Current Stock})}$ and categorizes as Fast, Slow, or Non-Moving. | High |
| **FR-04** | Fast Search | Instant search by item name, SKU, supplier, or specs with debounce and dynamic table updates. | High |
| **FR-05** | High Contrast | Toggle high-contrast theme delivering $\ge 7:1$ text contrast ratio and bold structural borders. | Critical (Q12) |
| **FR-06** | Font Scaling | Real-time font adjustment from 85% to 175% across all headings, table rows, and modal dialogs. | Critical (Q12) |
| **FR-07** | Keyboard Nav | Complete workflow operability via keyboard: <kbd>Alt+N</kbd> (New), <kbd>Alt+S</kbd> (Search), <kbd>Alt+H</kbd> (Contrast), <kbd>Alt+D</kbd> (Dark), <kbd>Alt+M</kbd> (Minimalist), <kbd>Arrows</kbd> (Rows). | Critical (Q12) |
| **FR-08** | Dark Mode | Balanced dark theme reducing glare for low-light laboratory operating environments. | Critical (Q12) |
| **FR-09** | Minimalist View | Toggle distraction-free layout hiding metric cards, banners, and decorative icons for cognitive clarity. | Critical (Q12) |
| **FR-10** | Audit Trail | Automated immutable logging of every addition, update, stock adjustment, and deletion. | Medium |
| **FR-11** | Data Portability | Export full catalog to CSV and JSON formats; import from JSON with schema validation. | Medium |

### 3.2 Non-Functional Requirements (NFR)

1. **Accessibility (NFR-A11Y):** Compliance with **WCAG 2.1 Level AA and AAA** guidelines:
   - Guideline 1.4.3 Contrast (Minimum): Normal text ratio $\ge 4.5:1$.
   - Guideline 1.4.6 Contrast (Enhanced): High contrast mode ratio $\ge 7.0:1$.
   - Guideline 2.1.1 Keyboard: 100% functionality accessible without pointing device.
   - Guideline 2.4.7 Focus Visible: Clear 3px high-contrast outline on all interactive controls.
2. **Performance (NFR-PERF):** Search and filter latency under 50 milliseconds across 1,000 catalog entries.
3. **Data Integrity (NFR-INT):** Zero duplicate SKU insertions via Poka-Yoke database constraints.
4. **Reliability & Recovery (NFR-REL):** Full state persistence across application reloads; automated recovery from corrupt input values.

---

## 4. Critical to Quality (CTQ) Parameters

Derived from laboratory user voice (Voice of Customer - VoC):

```
+-----------------------------------------------------------------------------------------+
|                               CRITICAL TO QUALITY (CTQ) TREE                            |
+-----------------------------------------------------------------------------------------+
| NEED: Dependable, inclusive lab equipment tracking that prevents student project delays |
+-----------------------------------------------------------------------------------------+
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
[Quality Driver 1]               [Quality Driver 2]               [Quality Driver 3]
Zero Lab Stockouts               Inclusive Accessibility          Frictionless Usability
        │                                │                                │
        ▼                                ▼                                ▼
[CTQ Metrics]                    [CTQ Metrics]                    [CTQ Metrics]
• Safety Stock: $\ge 5$ units    • Contrast Ratio: $\ge 7:1$      • Search Latency: $< 100$ms
• Stockout Rate: $0\%$           • Font Scalability: up to 175%   • Keyboard Navigation: 100%
• Auto ROP Alert: Instant        • Screen Reader ARIA: 100%       • Data Export: 1-Click CSV
```
