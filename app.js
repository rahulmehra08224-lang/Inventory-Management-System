/**
 * ============================================================================
 * Accessible Inventory Management System (Client-Side Application)
 * Student: Rahul Mehra | Dept: CSE AIML (Section B)
 * Project: Q12 Accessibility Suite
 * Features: High Contrast Mode, Dynamic Font Resizing, Comprehensive Keyboard
 * Navigation, Dark/Light Theming, Minimalist Cognitive Layout, ARIA Live Announcements
 * ============================================================================
 */

(function () {
  'use strict';

  // --------------------------------------------------------------------------
  // Default Sample Hardware Inventory Dataset (CSE AIML Lab Hardware)
  // --------------------------------------------------------------------------
  const DEFAULT_INVENTORY = [
    {
      id: "item-1",
      sku: "NV-JET-ORIN-8G",
      name: "NVIDIA Jetson Orin Nano Dev Kit (8GB)",
      category: "AI Accelerators",
      quantity: 12,
      minThreshold: 5,
      price: 44500.00,
      supplier: "NVIDIA Academic Direct",
      location: "Lab 402 - Cabinet A",
      specs: "40 TOPS AI, 6-core ARM Cortex-A78AE, Ampere GPU, 8GB 128-bit LPDDR5",
      updatedAt: "2026-10-28T10:30:00Z"
    },
    {
      id: "item-2",
      sku: "GGL-CORAL-USB",
      name: "Google Coral Edge TPU USB Accelerator",
      category: "AI Accelerators",
      quantity: 4,
      minThreshold: 6,
      price: 6800.00,
      supplier: "Google hardware partner",
      location: "Lab 402 - Shelf 2",
      specs: "4 TOPS Edge TPU ML coprocessor, USB 3.0 Type-C, TensorFlow Lite",
      updatedAt: "2026-10-27T14:15:00Z"
    },
    {
      id: "item-3",
      sku: "RPI-5-8GB-BRD",
      name: "Raspberry Pi 5 Model B (8GB RAM)",
      category: "Microcontrollers",
      quantity: 24,
      minThreshold: 8,
      price: 8200.00,
      supplier: "Element14 Distributors",
      location: "Lab 401 - Bin 04",
      specs: "Quad-core Cortex-A76 @ 2.4GHz, Dual 4Kp60 HDMI, PCIe 2.0 interface",
      updatedAt: "2026-10-28T09:00:00Z"
    },
    {
      id: "item-4",
      sku: "ARD-MEGA-2560",
      name: "Arduino Mega 2560 Rev3",
      category: "Microcontrollers",
      quantity: 18,
      minThreshold: 10,
      price: 3200.00,
      supplier: "Arduino Official Store",
      location: "Robotics Bench 1",
      specs: "ATmega2560, 54 digital I/O pins, 16 analog inputs, 4 UARTs",
      updatedAt: "2026-10-26T16:45:00Z"
    },
    {
      id: "item-5",
      sku: "INT-RS-D435I",
      name: "Intel RealSense Depth Camera D435i",
      category: "Sensors & Vision",
      quantity: 3,
      minThreshold: 4,
      price: 38500.00,
      supplier: "Intel Robotics Alliance",
      location: "Vision AI Workstation",
      specs: "Active IR stereo depth sensor, Integrated BMI055 6-DoF IMU, USB 3.1",
      updatedAt: "2026-10-28T11:20:00Z"
    },
    {
      id: "item-6",
      sku: "RPL-LIDAR-A1",
      name: "Slamtec RPLiDAR A1M8 360 Laser Scanner",
      category: "Sensors & Vision",
      quantity: 0,
      minThreshold: 3,
      price: 11900.00,
      supplier: "Slamtec Tech",
      location: "Autonomous Vehicle Bench",
      specs: "12-meter scanning range, 8000 samples/sec, 5.5Hz rotation rate",
      updatedAt: "2026-10-25T13:10:00Z"
    },
    {
      id: "item-7",
      sku: "LIPO-3S-5200",
      name: "Li-Po Battery Pack 11.1V 5200mAh 35C",
      category: "Power & Batteries",
      quantity: 7,
      minThreshold: 5,
      price: 3400.00,
      supplier: "Robu Power Systems",
      location: "Battery Safety Bunker",
      specs: "3-Cell (3S1P) Li-Polymer, XT60 connector, JST-XH balance plug",
      updatedAt: "2026-10-28T12:00:00Z"
    },
    {
      id: "item-8",
      sku: "MOT-TB6600-DRV",
      name: "TB6600 Stepper Motor Driver Controller",
      category: "Robotics & Actuators",
      quantity: 2,
      minThreshold: 6,
      price: 1150.00,
      supplier: "RoboElements",
      location: "CNC / 3D Printer Cart",
      specs: "4.0A 9-42VDC, micro-step 1/32, optocoupler signal isolation",
      updatedAt: "2026-10-26T17:00:00Z"
    },
    {
      id: "item-9",
      sku: "BME-680-ENV-SEN",
      name: "Bosch BME680 Environmental Sensor Breakout",
      category: "Sensors & Vision",
      quantity: 15,
      minThreshold: 5,
      price: 1950.00,
      supplier: "Adafruit Industries",
      location: "IoT Sensor Kit 3",
      specs: "Temperature, Humidity, Barometric Pressure, and VOC Gas sensing",
      updatedAt: "2026-10-27T08:30:00Z"
    },
    {
      id: "item-10",
      sku: "RIG-DS1054Z-OSC",
      name: "Rigol DS1054Z 50MHz 4-Channel Oscilloscope",
      category: "Lab Instruments",
      quantity: 5,
      minThreshold: 2,
      price: 36000.00,
      supplier: "Rigol Technologies",
      location: "Bench Instruments Bay",
      specs: "1 GSa/s real-time sample rate, 24 Mpts memory depth, 7-inch WVGA",
      updatedAt: "2026-10-24T15:20:00Z"
    }
  ];

  // --------------------------------------------------------------------------
  // Application State
  // --------------------------------------------------------------------------
  const STORAGE_KEYS = {
    INVENTORY: "rahul_aiml_inventory_data_v1",
    LOGS: "rahul_aiml_activity_logs_v1",
    A11Y_PREFS: "rahul_aiml_a11y_preferences_v1"
  };

  const state = {
    inventory: [],
    logs: [],
    filter: {
      search: "",
      category: "ALL",
      status: "ALL",
      sortBy: "name-asc"
    },
    a11y: {
      fontScale: 1.0,      // Available steps: 0.85, 1.0, 1.25, 1.5, 1.75
      contrast: "normal",  // "normal" or "high"
      theme: "light",      // "light" or "dark"
      layout: "standard"   // "standard" or "minimalist"
    },
    selectedRowIndex: -1,
    lastFocusedElement: null,
    pendingDeleteId: null
  };

  // --------------------------------------------------------------------------
  // DOM Elements Cache
  // --------------------------------------------------------------------------
  const DOM = {
    html: document.documentElement,
    ariaAnnouncer: document.getElementById("aria-announcer"),

    // A11y Toolbar Controls
    btnFontDecrease: document.getElementById("btn-font-decrease"),
    btnFontIncrease: document.getElementById("btn-font-increase"),
    btnFontReset: document.getElementById("btn-font-reset"),
    fontSizeIndicator: document.getElementById("font-size-indicator"),
    btnToggleContrast: document.getElementById("btn-toggle-contrast"),
    btnToggleTheme: document.getElementById("btn-toggle-theme"),
    themeIcon: document.getElementById("theme-icon"),
    themeText: document.getElementById("theme-text"),
    btnToggleMinimalist: document.getElementById("btn-toggle-minimalist"),
    minimalistText: document.getElementById("minimalist-text"),
    minimalistBanner: document.getElementById("minimalist-banner"),
    btnExitMinimalist: document.getElementById("btn-exit-minimalist"),
    btnOpenShortcuts: document.getElementById("btn-open-shortcuts"),
    btnOpenA11yInfo: document.getElementById("btn-open-a11y-info"),

    // Metrics
    statTotalSkus: document.getElementById("stat-total-skus"),
    statTotalStock: document.getElementById("stat-total-stock"),
    statInventoryVal: document.getElementById("stat-inventory-val"),
    statLowStock: document.getElementById("stat-low-stock"),

    // Filters & Search
    searchInput: document.getElementById("search-input"),
    btnClearSearch: document.getElementById("btn-clear-search"),
    filterCategory: document.getElementById("filter-category"),
    filterStatus: document.getElementById("filter-status"),
    sortBy: document.getElementById("sort-by"),
    resultsCount: document.getElementById("results-count"),
    activeFilterTags: document.getElementById("active-filter-tags"),
    btnResetFilters: document.getElementById("btn-reset-filters"),
    btnResetSampleData: document.getElementById("btn-reset-sample-data"),

    // Table
    table: document.getElementById("inventory-table"),
    tableBody: document.getElementById("inventory-table-body"),
    tableWrapper: document.querySelector(".table-scroll-wrapper"),
    emptyState: document.getElementById("empty-state"),
    btnEmptyClear: document.getElementById("btn-empty-clear"),

    // Activity Log
    activityLogList: document.getElementById("activity-log-list"),
    btnClearLogs: document.getElementById("btn-clear-logs"),

    // Global Actions
    btnAddItem: document.getElementById("btn-add-item"),
    btnExportCsv: document.getElementById("btn-export-csv"),
    btnExportJson: document.getElementById("btn-export-json"),
    importFile: document.getElementById("import-file"),

    // Item Form Modal
    modalItemForm: document.getElementById("modal-item-form"),
    modalFormTitle: document.getElementById("modal-form-title"),
    btnCloseModalForm: document.getElementById("btn-close-modal-form"),
    btnCancelForm: document.getElementById("btn-cancel-form"),
    itemForm: document.getElementById("item-form"),
    formItemId: document.getElementById("form-item-id"),
    formSku: document.getElementById("form-sku"),
    formCategory: document.getElementById("form-category"),
    formName: document.getElementById("form-name"),
    formQuantity: document.getElementById("form-quantity"),
    formMinThreshold: document.getElementById("form-min-threshold"),
    formPrice: document.getElementById("form-price"),
    formSupplier: document.getElementById("form-supplier"),
    formLocation: document.getElementById("form-location"),
    formNotes: document.getElementById("form-notes"),

    // Delete Modal
    modalDeleteConfirm: document.getElementById("modal-delete-confirm"),
    delItemName: document.getElementById("del-item-name"),
    btnCloseDeleteModal: document.getElementById("btn-close-delete-modal"),
    btnCancelDelete: document.getElementById("btn-cancel-delete"),
    btnConfirmDelete: document.getElementById("btn-confirm-delete"),

    // Shortcuts Modal
    modalShortcuts: document.getElementById("modal-shortcuts"),
    btnCloseShortcutsModal: document.getElementById("btn-close-shortcuts-modal"),
    btnDismissShortcuts: document.getElementById("btn-dismiss-shortcuts"),

    // A11y Info Modal
    modalA11yInfo: document.getElementById("modal-a11y-info"),
    btnCloseA11yModal: document.getElementById("btn-close-a11y-modal"),
    btnDismissA11yInfo: document.getElementById("btn-dismiss-a11y-info")
  };

  // --------------------------------------------------------------------------
  // ARIA Live Announcements (Polite & Assertive)
  // --------------------------------------------------------------------------
  function announce(message, priority = "polite") {
    if (!DOM.ariaAnnouncer) return;
    DOM.ariaAnnouncer.setAttribute("aria-live", priority);
    // Clear first to re-trigger if same text
    DOM.ariaAnnouncer.textContent = "";
    setTimeout(() => {
      DOM.ariaAnnouncer.textContent = message;
    }, 50);
  }

  // --------------------------------------------------------------------------
  // Accessibility Engine (Font Resizing, Contrast, Theme, Minimalist Mode)
  // --------------------------------------------------------------------------
  const FONT_SCALES = [0.85, 1.0, 1.25, 1.5, 1.75];

  function setFontScale(newScale, announceChange = true) {
    // Clamp to valid range
    const clampedScale = Math.min(1.75, Math.max(0.85, Math.round(newScale * 100) / 100));
    state.a11y.fontScale = clampedScale;

    DOM.html.style.setProperty("--font-scale", clampedScale);
    const percent = Math.round(clampedScale * 100) + "%";
    DOM.fontSizeIndicator.textContent = percent;
    DOM.btnFontDecrease.setAttribute("aria-label", `Decrease Font Size (Current scale: ${percent})`);
    DOM.btnFontIncrease.setAttribute("aria-label", `Increase Font Size (Current scale: ${percent})`);

    saveA11yPreferences();
    if (announceChange) {
      announce(`Font size adjusted to ${percent}`);
    }
  }

  function stepFont(direction) {
    const currentIndex = FONT_SCALES.findIndex(s => Math.abs(s - state.a11y.fontScale) < 0.05);
    let nextIndex = currentIndex !== -1 ? currentIndex + direction : 1 + direction;
    nextIndex = Math.max(0, Math.min(FONT_SCALES.length - 1, nextIndex));
    setFontScale(FONT_SCALES[nextIndex], true);
  }

  function toggleHighContrast(forceValue = null) {
    const isCurrentlyHigh = state.a11y.contrast === "high";
    const nextState = forceValue !== null ? forceValue : !isCurrentlyHigh;
    state.a11y.contrast = nextState ? "high" : "normal";

    DOM.html.setAttribute("data-contrast", state.a11y.contrast);
    DOM.btnToggleContrast.setAttribute("aria-pressed", nextState ? "true" : "false");

    saveA11yPreferences();
    announce(nextState ? "High contrast mode enabled." : "Standard contrast mode restored.");
  }

  function toggleTheme(forceTheme = null) {
    const nextTheme = forceTheme || (state.a11y.theme === "dark" ? "light" : "dark");
    state.a11y.theme = nextTheme;

    DOM.html.setAttribute("data-theme", nextTheme);
    const isDark = nextTheme === "dark";
    DOM.btnToggleTheme.setAttribute("aria-pressed", isDark ? "true" : "false");
    DOM.themeIcon.innerHTML = isDark ? "&#9788;" : "&#9790;";
    DOM.themeText.textContent = isDark ? "Light Mode" : "Dark Mode";

    saveA11yPreferences();
    announce(`${isDark ? "Dark" : "Light"} mode active.`);
  }

  function toggleMinimalistLayout(forceValue = null) {
    const isCurrentlyMinimal = state.a11y.layout === "minimalist";
    const nextState = forceValue !== null ? forceValue : !isCurrentlyMinimal;
    state.a11y.layout = nextState ? "minimalist" : "standard";

    DOM.html.setAttribute("data-layout", state.a11y.layout);
    DOM.btnToggleMinimalist.setAttribute("aria-pressed", nextState ? "true" : "false");
    DOM.minimalistBanner.style.display = nextState ? "flex" : "none";

    saveA11yPreferences();
    announce(
      nextState
        ? "Minimalist layout mode activated. Visual clutter and secondary widgets hidden."
        : "Standard full layout view restored."
    );
  }

  function saveA11yPreferences() {
    try {
      localStorage.setItem(STORAGE_KEYS.A11Y_PREFS, JSON.stringify(state.a11y));
    } catch (e) {
      console.warn("Unable to save accessibility preferences to localStorage", e);
    }
  }

  function loadA11yPreferences() {
    try {
      const saved = localStorage.getItem(STORAGE_KEYS.A11Y_PREFS);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed.fontScale) setFontScale(parsed.fontScale, false);
        if (parsed.contrast) toggleHighContrast(parsed.contrast === "high");
        if (parsed.theme) toggleTheme(parsed.theme);
        if (parsed.layout) toggleMinimalistLayout(parsed.layout === "minimalist");
      }
    } catch (e) {
      console.warn("Unable to read saved accessibility preferences", e);
    }
  }

  // --------------------------------------------------------------------------
  // Accessible Modal Management & Focus Traps (WCAG 2.4.3 & 2.1.2)
  // --------------------------------------------------------------------------
  function openModal(modalElement, triggerElement = null) {
    state.lastFocusedElement = triggerElement || document.activeElement;
    modalElement.removeAttribute("hidden");
    document.body.style.overflow = "hidden"; // Prevent background scroll

    // Find first focusable element inside modal
    const focusable = getFocusableElements(modalElement);
    if (focusable.length > 0) {
      setTimeout(() => focusable[0].focus(), 50);
    }

    announce(`Dialog opened: ${modalElement.querySelector(".modal-title")?.textContent || "Modal"}`);
  }

  function closeModal(modalElement) {
    modalElement.setAttribute("hidden", "");
    document.body.style.overflow = "";

    // Return focus to trigger element
    if (state.lastFocusedElement && typeof state.lastFocusedElement.focus === "function") {
      state.lastFocusedElement.focus();
    }
  }

  function getFocusableElements(container) {
    return Array.from(
      container.querySelectorAll(
        'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
      )
    ).filter(el => el.offsetWidth > 0 || el.offsetHeight > 0);
  }

  function trapFocusInModal(e, modalElement) {
    if (e.key !== "Tab") return;
    const focusable = getFocusableElements(modalElement);
    if (focusable.length === 0) return;

    const firstElement = focusable[0];
    const lastElement = focusable[focusable.length - 1];

    if (e.shiftKey) {
      // Shift + Tab
      if (document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      }
    } else {
      // Tab
      if (document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
  }

  // --------------------------------------------------------------------------
  // Global Keyboard Shortcuts (WCAG 2.1.4)
  // --------------------------------------------------------------------------
  function initKeyboardShortcuts() {
    window.addEventListener("keydown", (e) => {
      // Check if user is typing in an input, textarea, or select (unless using Alt shortcuts or Esc)
      const isInputFocused = ["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName);

      // ESCAPE key: Close any active modal or clear search
      if (e.key === "Escape") {
        if (!DOM.modalItemForm.hasAttribute("hidden")) {
          e.preventDefault();
          closeModal(DOM.modalItemForm);
          return;
        }
        if (!DOM.modalDeleteConfirm.hasAttribute("hidden")) {
          e.preventDefault();
          closeModal(DOM.modalDeleteConfirm);
          return;
        }
        if (!DOM.modalShortcuts.hasAttribute("hidden")) {
          e.preventDefault();
          closeModal(DOM.modalShortcuts);
          return;
        }
        if (!DOM.modalA11yInfo.hasAttribute("hidden")) {
          e.preventDefault();
          closeModal(DOM.modalA11yInfo);
          return;
        }
        if (DOM.searchInput.value) {
          e.preventDefault();
          clearSearch();
          return;
        }
      }

      // '?' key: Open Shortcuts cheat sheet (when not in a text input)
      if (e.key === "?" && !isInputFocused) {
        e.preventDefault();
        openModal(DOM.modalShortcuts, DOM.btnOpenShortcuts);
        return;
      }

      // ALT + combinations
      if (e.altKey && !e.ctrlKey && !e.metaKey) {
        switch (e.key.toLowerCase()) {
          case "n": // Alt + N: New Item
            e.preventDefault();
            openAddItemModal();
            break;

          case "s": // Alt + S: Focus Search
            e.preventDefault();
            DOM.searchInput.focus();
            DOM.searchInput.select();
            announce("Search input focused.");
            break;

          case "h": // Alt + H: High Contrast Toggle
            e.preventDefault();
            toggleHighContrast();
            break;

          case "d": // Alt + D: Dark Mode Toggle
            e.preventDefault();
            toggleTheme();
            break;

          case "m": // Alt + M: Minimalist Mode Toggle
            e.preventDefault();
            toggleMinimalistLayout();
            break;

          case "+":
          case "=": // Alt + +: Increase font
            e.preventDefault();
            stepFont(1);
            break;

          case "-":
          case "_": // Alt + -: Decrease font
            e.preventDefault();
            stepFont(-1);
            break;

          case "0": // Alt + 0: Reset font
            e.preventDefault();
            setFontScale(1.0, true);
            break;

          case "e": // Alt + E: Export to CSV
            e.preventDefault();
            exportToCSV();
            break;

          case "r": // Alt + R: Reset to Demo dataset
            e.preventDefault();
            resetSampleData();
            break;
        }
      }
    });

    // Modal trap listeners
    [DOM.modalItemForm, DOM.modalDeleteConfirm, DOM.modalShortcuts, DOM.modalA11yInfo].forEach(modal => {
      modal.addEventListener("keydown", (e) => trapFocusInModal(e, modal));
      // Close on backdrop click
      modal.addEventListener("click", (e) => {
        if (e.target === modal) {
          closeModal(modal);
        }
      });
    });

    // Table Arrow Navigation
    DOM.tableWrapper.addEventListener("keydown", handleTableArrowNavigation);
  }

  function handleTableArrowNavigation(e) {
    const rows = Array.from(DOM.tableBody.querySelectorAll("tr"));
    if (rows.length === 0) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      state.selectedRowIndex = Math.min(rows.length - 1, state.selectedRowIndex + 1);
      highlightRow(rows, state.selectedRowIndex);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      state.selectedRowIndex = Math.max(0, state.selectedRowIndex - 1);
      highlightRow(rows, state.selectedRowIndex);
    } else if (e.key === "Enter" && state.selectedRowIndex >= 0) {
      // Trigger edit on selected row
      const currentRow = rows[state.selectedRowIndex];
      const editBtn = currentRow?.querySelector(".btn-action-edit");
      if (editBtn) {
        e.preventDefault();
        editBtn.click();
      }
    }
  }

  function highlightRow(rows, index) {
    rows.forEach((row, i) => {
      if (i === index) {
        row.classList.add("is-selected");
        row.focus();
        const itemName = row.querySelector("strong")?.textContent || "Item";
        const stock = row.querySelector(".stock-value")?.textContent || "0";
        announce(`Row ${i + 1} of ${rows.length}: ${itemName}, ${stock} units. Press Enter to edit.`);
      } else {
        row.classList.remove("is-selected");
      }
    });
  }

  // --------------------------------------------------------------------------
  // Inventory Data & Local Storage Persistence
  // --------------------------------------------------------------------------
  function loadInventoryData() {
    try {
      const stored = localStorage.getItem(STORAGE_KEYS.INVENTORY);
      if (stored) {
        state.inventory = JSON.parse(stored);
      } else {
        state.inventory = [...DEFAULT_INVENTORY];
        saveInventoryData();
      }
    } catch (e) {
      console.warn("Failed loading from localStorage, using defaults", e);
      state.inventory = [...DEFAULT_INVENTORY];
    }

    try {
      const storedLogs = localStorage.getItem(STORAGE_KEYS.LOGS);
      state.logs = storedLogs ? JSON.parse(storedLogs) : [];
      if (state.logs.length === 0) {
        logActivity("System initialized with CSE AIML hardware catalog.");
      }
    } catch (e) {
      state.logs = [];
    }
  }

  function saveInventoryData() {
    try {
      localStorage.setItem(STORAGE_KEYS.INVENTORY, JSON.stringify(state.inventory));
    } catch (e) {
      console.error("Unable to save inventory data", e);
    }
  }

  function logActivity(actionText) {
    const entry = {
      id: "log-" + Date.now(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
      text: actionText
    };
    state.logs.unshift(entry);
    if (state.logs.length > 30) state.logs.pop(); // Keep recent 30
    try {
      localStorage.setItem(STORAGE_KEYS.LOGS, JSON.stringify(state.logs));
    } catch (e) {}
    renderActivityLogs();
  }

  function renderActivityLogs() {
    DOM.activityLogList.innerHTML = "";
    if (state.logs.length === 0) {
      DOM.activityLogList.innerHTML = `<li class="log-item"><span class="log-timestamp">--</span> No recent activity.</li>`;
      return;
    }
    state.logs.forEach(log => {
      const li = document.createElement("li");
      li.className = "log-item";
      li.innerHTML = `<span class="log-timestamp">[${log.timestamp}]</span> <span>${escapeHtml(log.text)}</span>`;
      DOM.activityLogList.appendChild(li);
    });
  }

  // --------------------------------------------------------------------------
  // Table Rendering & Filtering Engine
  // --------------------------------------------------------------------------
  function getFilteredAndSortedInventory() {
    let result = state.inventory.filter(item => {
      // Search filter (Name, SKU, Supplier, Specs)
      if (state.filter.search.trim()) {
        const q = state.filter.search.toLowerCase().trim();
        const matchesName = item.name.toLowerCase().includes(q);
        const matchesSku = item.sku.toLowerCase().includes(q);
        const matchesSupplier = (item.supplier || "").toLowerCase().includes(q);
        const matchesSpecs = (item.specs || "").toLowerCase().includes(q);
        if (!matchesName && !matchesSku && !matchesSupplier && !matchesSpecs) {
          return false;
        }
      }

      // Category filter
      if (state.filter.category !== "ALL" && item.category !== state.filter.category) {
        return false;
      }

      // Stock status filter
      if (state.filter.status !== "ALL") {
        const isOutOfStock = item.quantity === 0;
        const isLowStock = item.quantity > 0 && item.quantity <= item.minThreshold;
        const isInStock = item.quantity > item.minThreshold;

        if (state.filter.status === "OUT_OF_STOCK" && !isOutOfStock) return false;
        if (state.filter.status === "LOW_STOCK" && !isLowStock) return false;
        if (state.filter.status === "IN_STOCK" && !isInStock) return false;
      }

      return true;
    });

    // Sort order
    result.sort((a, b) => {
      switch (state.filter.sortBy) {
        case "name-asc":
          return a.name.localeCompare(b.name);
        case "name-desc":
          return b.name.localeCompare(a.name);
        case "qty-asc":
          return a.quantity - b.quantity;
        case "qty-desc":
          return b.quantity - a.quantity;
        case "price-asc":
          return a.price - b.price;
        case "price-desc":
          return b.price - a.price;
        case "date-desc":
        default:
          return new Date(b.updatedAt || 0) - new Date(a.updatedAt || 0);
      }
    });

    return result;
  }

  function renderTable() {
    const items = getFilteredAndSortedInventory();
    DOM.tableBody.innerHTML = "";
    state.selectedRowIndex = -1;

    // Update Counts & Filter Status
    DOM.resultsCount.textContent = `Showing ${items.length} of ${state.inventory.length} inventory items`;
    updateActiveFilterPills();

    // Toggle Empty State
    if (items.length === 0) {
      DOM.emptyState.style.display = "block";
      DOM.table.style.display = "none";
    } else {
      DOM.emptyState.style.display = "none";
      DOM.table.style.display = "table";

      items.forEach((item, index) => {
        const row = createTableRow(item, index);
        DOM.tableBody.appendChild(row);
      });
    }

    updateMetricsSummary();
  }

  function createTableRow(item, index) {
    const tr = document.createElement("tr");
    tr.tabIndex = 0; // Focusable for keyboard navigation
    tr.dataset.itemId = item.id;
    tr.setAttribute("aria-label", `${item.name}, SKU ${item.sku}, Stock ${item.quantity} units, Price ₹${item.price.toFixed(2)}`);

    // Determine status badge
    let statusBadge = "";
    if (item.quantity === 0) {
      statusBadge = `<span class="badge badge-out-of-stock" aria-label="Status: Out of Stock"><span aria-hidden="true">&times;</span> Out of Stock</span>`;
    } else if (item.quantity <= item.minThreshold) {
      statusBadge = `<span class="badge badge-low-stock" aria-label="Status: Low Stock, at or below threshold"><span aria-hidden="true">&#9888;</span> Low (${item.quantity}/${item.minThreshold})</span>`;
    } else {
      statusBadge = `<span class="badge badge-in-stock" aria-label="Status: In Stock"><span aria-hidden="true">&#10003;</span> In Stock</span>`;
    }

    tr.innerHTML = `
      <td class="th-sku">
        <span class="sku-code">${escapeHtml(item.sku)}</span>
      </td>
      <td class="th-name">
        <div class="item-name-cell">
          <strong>${escapeHtml(item.name)}</strong>
          ${item.specs ? `<span class="item-specs">${escapeHtml(item.specs)}</span>` : ""}
        </div>
      </td>
      <td class="th-cat">
        <span>${escapeHtml(item.category)}</span>
      </td>
      <td class="th-qty">
        <div class="stock-control-cell">
          <button type="button" class="btn-stock-step btn-decrement" data-id="${item.id}" title="Decrease stock by 1" aria-label="Decrease stock for ${escapeHtml(item.name)} by 1">
            <span aria-hidden="true">-</span>
          </button>
          <span class="stock-value" aria-live="polite">${item.quantity}</span>
          <button type="button" class="btn-stock-step btn-increment" data-id="${item.id}" title="Increase stock by 1" aria-label="Increase stock for ${escapeHtml(item.name)} by 1">
            <span aria-hidden="true">+</span>
          </button>
        </div>
      </td>
      <td class="th-status">
        ${statusBadge}
      </td>
      <td class="th-price">
        <strong>₹${item.price.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong>
      </td>
      <td class="th-supplier">
        <div>${escapeHtml(item.supplier || "N/A")}</div>
        ${item.location ? `<small class="text-muted" style="font-size:0.75rem">${escapeHtml(item.location)}</small>` : ""}
      </td>
      <td class="th-actions">
        <div class="table-row-actions">
          <button type="button" class="btn-action btn-action-edit" data-id="${item.id}" aria-label="Edit details for ${escapeHtml(item.name)}">
            Edit
          </button>
          <button type="button" class="btn-action btn-action-delete" data-id="${item.id}" aria-label="Delete ${escapeHtml(item.name)} from inventory">
            Delete
          </button>
        </div>
      </td>
    `;

    // Event Listeners for Stock Adjustments
    const btnDec = tr.querySelector(".btn-decrement");
    const btnInc = tr.querySelector(".btn-increment");
    const btnEdit = tr.querySelector(".btn-action-edit");
    const btnDel = tr.querySelector(".btn-action-delete");

    btnDec.addEventListener("click", () => adjustStock(item.id, -1));
    btnInc.addEventListener("click", () => adjustStock(item.id, +1));
    btnEdit.addEventListener("click", () => openEditItemModal(item.id, btnEdit));
    btnDel.addEventListener("click", () => promptDeleteItem(item.id, btnDel));

    return tr;
  }

  function adjustStock(itemId, delta) {
    const item = state.inventory.find(i => i.id === itemId);
    if (!item) return;

    const oldQty = item.quantity;
    const newQty = Math.max(0, oldQty + delta);
    if (oldQty === newQty) return;

    item.quantity = newQty;
    item.updatedAt = new Date().toISOString();
    saveInventoryData();

    logActivity(`Adjusted stock of "${item.name}" from ${oldQty} to ${newQty}.`);
    announce(`Stock for ${item.name} updated to ${newQty} units.`);
    renderTable();
  }

  function updateMetricsSummary() {
    const totalSkus = state.inventory.length;
    const totalStock = state.inventory.reduce((sum, item) => sum + (Number(item.quantity) || 0), 0);
    const totalVal = state.inventory.reduce((sum, item) => sum + ((Number(item.quantity) || 0) * (Number(item.price) || 0)), 0);
    const lowStockCount = state.inventory.filter(item => item.quantity <= item.minThreshold).length;

    DOM.statTotalSkus.textContent = totalSkus;
    DOM.statTotalStock.textContent = totalStock;
    DOM.statInventoryVal.textContent = "₹" + totalVal.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    DOM.statLowStock.textContent = lowStockCount;
  }

  function updateActiveFilterPills() {
    DOM.activeFilterTags.innerHTML = "";
    let hasActiveFilters = false;

    if (state.filter.search.trim()) {
      hasActiveFilters = true;
      const pill = document.createElement("span");
      pill.className = "filter-pill";
      pill.textContent = `Search: "${state.filter.search.trim()}"`;
      DOM.activeFilterTags.appendChild(pill);
    }

    if (state.filter.category !== "ALL") {
      hasActiveFilters = true;
      const pill = document.createElement("span");
      pill.className = "filter-pill";
      pill.textContent = `Cat: ${state.filter.category}`;
      DOM.activeFilterTags.appendChild(pill);
    }

    if (state.filter.status !== "ALL") {
      hasActiveFilters = true;
      const pill = document.createElement("span");
      pill.className = "filter-pill";
      pill.textContent = `Status: ${state.filter.status}`;
      DOM.activeFilterTags.appendChild(pill);
    }

    DOM.btnResetFilters.style.display = hasActiveFilters ? "inline-block" : "none";
  }

  function clearSearch() {
    state.filter.search = "";
    DOM.searchInput.value = "";
    DOM.btnClearSearch.style.display = "none";
    renderTable();
    announce("Search filter cleared.");
  }

  function resetFilters() {
    state.filter.search = "";
    state.filter.category = "ALL";
    state.filter.status = "ALL";
    state.filter.sortBy = "name-asc";

    DOM.searchInput.value = "";
    DOM.btnClearSearch.style.display = "none";
    DOM.filterCategory.value = "ALL";
    DOM.filterStatus.value = "ALL";
    DOM.sortBy.value = "name-asc";

    renderTable();
    announce("All search and filter criteria have been reset.");
  }

  function resetSampleData() {
    if (confirm("Reset inventory back to original CSE AIML hardware sample dataset? Any unsaved additions will be overwritten.")) {
      state.inventory = JSON.parse(JSON.stringify(DEFAULT_INVENTORY));
      saveInventoryData();
      logActivity("Reset catalog to default CSE AIML hardware dataset.");
      renderTable();
      announce("Inventory reset to default sample dataset.");
    }
  }

  // --------------------------------------------------------------------------
  // Add / Edit Modal & Accessible Form Validation
  // --------------------------------------------------------------------------
  function openAddItemModal() {
    DOM.modalFormTitle.textContent = "Add New Hardware Item";
    DOM.itemForm.reset();
    DOM.formItemId.value = "";
    clearFormErrors();
    openModal(DOM.modalItemForm, DOM.btnAddItem);
  }

  function openEditItemModal(itemId, triggerBtn) {
    const item = state.inventory.find(i => i.id === itemId);
    if (!item) return;

    DOM.modalFormTitle.textContent = `Edit Item: ${item.name}`;
    DOM.formItemId.value = item.id;
    DOM.formSku.value = item.sku;
    DOM.formCategory.value = item.category;
    DOM.formName.value = item.name;
    DOM.formQuantity.value = item.quantity;
    DOM.formMinThreshold.value = item.minThreshold;
    DOM.formPrice.value = item.price;
    DOM.formSupplier.value = item.supplier || "";
    DOM.formLocation.value = item.location || "";
    DOM.formNotes.value = item.specs || "";

    clearFormErrors();
    openModal(DOM.modalItemForm, triggerBtn);
  }

  function clearFormErrors() {
    const errorSpans = DOM.itemForm.querySelectorAll(".form-error");
    errorSpans.forEach(span => (span.textContent = ""));
    const inputs = DOM.itemForm.querySelectorAll(".form-input");
    inputs.forEach(input => {
      input.classList.remove("is-invalid");
      input.removeAttribute("aria-invalid");
    });
  }

  function setFieldError(fieldId, errorMsg) {
    const field = document.getElementById(fieldId);
    const errorSpan = document.getElementById(fieldId.replace("form-", "") + "-error");
    if (field) {
      field.classList.add("is-invalid");
      field.setAttribute("aria-invalid", "true");
    }
    if (errorSpan) {
      errorSpan.textContent = errorMsg;
    }
  }

  function handleFormSubmit(e) {
    e.preventDefault();
    clearFormErrors();

    const id = DOM.formItemId.value.trim();
    const sku = DOM.formSku.value.trim().toUpperCase();
    const category = DOM.formCategory.value.trim();
    const name = DOM.formName.value.trim();
    const quantity = parseInt(DOM.formQuantity.value, 10);
    const minThreshold = parseInt(DOM.formMinThreshold.value, 10);
    const price = parseFloat(DOM.formPrice.value);
    const supplier = DOM.formSupplier.value.trim();
    const location = DOM.formLocation.value.trim();
    const specs = DOM.formNotes.value.trim();

    let hasErrors = false;

    // Validate SKU
    if (!sku) {
      setFieldError("form-sku", "SKU / Asset Code is required.");
      hasErrors = true;
    } else {
      // Check for SKU uniqueness (excluding editing self)
      const duplicate = state.inventory.find(i => i.sku.toUpperCase() === sku && i.id !== id);
      if (duplicate) {
        setFieldError("form-sku", `SKU "${sku}" is already assigned to "${duplicate.name}".`);
        hasErrors = true;
      }
    }

    // Validate Category
    if (!category) {
      setFieldError("form-category", "Please select a category.");
      hasErrors = true;
    }

    // Validate Name
    if (!name) {
      setFieldError("form-name", "Item name is required.");
      hasErrors = true;
    }

    // Validate Quantity
    if (isNaN(quantity) || quantity < 0) {
      setFieldError("form-quantity", "Quantity must be a positive integer (0 or more).");
      hasErrors = true;
    }

    // Validate Min Threshold
    if (isNaN(minThreshold) || minThreshold < 1) {
      setFieldError("form-min-threshold", "Alert threshold must be at least 1.");
      hasErrors = true;
    }

    // Validate Price
    if (isNaN(price) || price < 0) {
      setFieldError("form-price", "Price must be a valid non-negative number.");
      hasErrors = true;
    }

    if (hasErrors) {
      const firstInvalid = DOM.itemForm.querySelector(".is-invalid");
      if (firstInvalid) firstInvalid.focus();
      announce("Form submission has errors. Please correct the highlighted fields.", "assertive");
      return;
    }

    // Save or Update Item
    if (id) {
      // Edit existing
      const existing = state.inventory.find(i => i.id === id);
      if (existing) {
        existing.sku = sku;
        existing.category = category;
        existing.name = name;
        existing.quantity = quantity;
        existing.minThreshold = minThreshold;
        existing.price = price;
        existing.supplier = supplier;
        existing.location = location;
        existing.specs = specs;
        existing.updatedAt = new Date().toISOString();

        logActivity(`Updated item: "${name}" (${sku}).`);
        announce(`Successfully updated ${name}.`);
      }
    } else {
      // Add new
      const newItem = {
        id: "item-" + Date.now(),
        sku,
        category,
        name,
        quantity,
        minThreshold,
        price,
        supplier,
        location,
        specs,
        updatedAt: new Date().toISOString()
      };
      state.inventory.unshift(newItem);
      logActivity(`Added new inventory item: "${name}" (${sku}).`);
      announce(`Successfully added ${name} to inventory.`);
    }

    saveInventoryData();
    closeModal(DOM.modalItemForm);
    renderTable();
  }

  // --------------------------------------------------------------------------
  // Delete Confirmation Dialog
  // --------------------------------------------------------------------------
  function promptDeleteItem(itemId, triggerBtn) {
    const item = state.inventory.find(i => i.id === itemId);
    if (!item) return;

    state.pendingDeleteId = itemId;
    DOM.delItemName.textContent = `"${item.name}" (SKU: ${item.sku})`;
    openModal(DOM.modalDeleteConfirm, triggerBtn);
  }

  function confirmDeleteItem() {
    if (!state.pendingDeleteId) return;

    const item = state.inventory.find(i => i.id === state.pendingDeleteId);
    if (item) {
      const itemName = item.name;
      state.inventory = state.inventory.filter(i => i.id !== state.pendingDeleteId);
      saveInventoryData();

      logActivity(`Deleted item: "${itemName}".`);
      announce(`Item "${itemName}" has been permanently removed.`);
    }

    state.pendingDeleteId = null;
    closeModal(DOM.modalDeleteConfirm);
    renderTable();
  }

  // --------------------------------------------------------------------------
  // Export to CSV & JSON & File Import
  // --------------------------------------------------------------------------
  function exportToCSV() {
    const headers = ["SKU", "Item Name", "Category", "Quantity", "Min Threshold", "Unit Price (INR)", "Status", "Supplier", "Location", "Specs"];
    const rows = state.inventory.map(item => {
      let status = "In Stock";
      if (item.quantity === 0) status = "Out of Stock";
      else if (item.quantity <= item.minThreshold) status = "Low Stock";

      return [
        `"${item.sku.replace(/"/g, '""')}"`,
        `"${item.name.replace(/"/g, '""')}"`,
        `"${item.category.replace(/"/g, '""')}"`,
        item.quantity,
        item.minThreshold,
        item.price.toFixed(2),
        `"${status}"`,
        `"${(item.supplier || "").replace(/"/g, '""')}"`,
        `"${(item.location || "").replace(/"/g, '""')}"`,
        `"${(item.specs || "").replace(/"/g, '""')}"`
      ].join(",");
    });

    const csvContent = "\uFEFF" + [headers.join(","), ...rows].join("\r\n");
    downloadFile(csvContent, "text/csv;charset=utf-8;", `inventory-export-${formatDateForFilename(new Date())}.csv`);
    logActivity("Exported catalog to CSV file.");
    announce("Inventory catalog exported to CSV successfully.");
  }

  function exportToJSON() {
    const dataStr = JSON.stringify(state.inventory, null, 2);
    downloadFile(dataStr, "application/json", `inventory-data-${formatDateForFilename(new Date())}.json`);
    logActivity("Exported catalog to JSON file.");
    announce("Inventory catalog exported to JSON file.");
  }

  function handleImportJSON(e) {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (evt) {
      try {
        const imported = JSON.parse(evt.target.result);
        if (Array.isArray(imported)) {
          // Validate structure
          const validItems = imported.filter(i => i.sku && i.name && typeof i.quantity !== "undefined");
          if (validItems.length > 0) {
            state.inventory = validItems;
            saveInventoryData();
            logActivity(`Imported ${validItems.length} items from JSON file.`);
            renderTable();
            announce(`Successfully imported ${validItems.length} inventory items.`);
          } else {
            alert("No valid inventory records found in the uploaded JSON file.");
          }
        } else {
          alert("Uploaded JSON must be an array of inventory items.");
        }
      } catch (err) {
        alert("Failed to parse JSON file: " + err.message);
      }
    };
    reader.readAsText(file);
    e.target.value = ""; // Reset file input
  }

  function downloadFile(content, mimeType, filename) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function formatDateForFilename(date) {
    return date.toISOString().slice(0, 10);
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // --------------------------------------------------------------------------
  // Event Bindings Initialization
  // --------------------------------------------------------------------------
  function initEvents() {
    // Accessibility Toolbar Buttons
    DOM.btnFontDecrease.addEventListener("click", () => stepFont(-1));
    DOM.btnFontIncrease.addEventListener("click", () => stepFont(1));
    DOM.btnFontReset.addEventListener("click", () => setFontScale(1.0, true));
    DOM.btnToggleContrast.addEventListener("click", () => toggleHighContrast());
    DOM.btnToggleTheme.addEventListener("click", () => toggleTheme());
    DOM.btnToggleMinimalist.addEventListener("click", () => toggleMinimalistLayout());
    DOM.btnExitMinimalist.addEventListener("click", () => toggleMinimalistLayout(false));

    // Shortcut & A11y Info Dialogs
    DOM.btnOpenShortcuts.addEventListener("click", () => openModal(DOM.modalShortcuts, DOM.btnOpenShortcuts));
    DOM.btnCloseShortcutsModal.addEventListener("click", () => closeModal(DOM.modalShortcuts));
    DOM.btnDismissShortcuts.addEventListener("click", () => closeModal(DOM.modalShortcuts));

    DOM.btnOpenA11yInfo.addEventListener("click", () => openModal(DOM.modalA11yInfo, DOM.btnOpenA11yInfo));
    DOM.btnCloseA11yModal.addEventListener("click", () => closeModal(DOM.modalA11yInfo));
    DOM.btnDismissA11yInfo.addEventListener("click", () => closeModal(DOM.modalA11yInfo));

    // Global Top Actions
    DOM.btnAddItem.addEventListener("click", openAddItemModal);
    DOM.btnExportCsv.addEventListener("click", exportToCSV);
    DOM.btnExportJson.addEventListener("click", exportToJSON);
    DOM.importFile.addEventListener("change", handleImportJSON);

    // Filter & Search Controls
    DOM.searchInput.addEventListener("input", (e) => {
      state.filter.search = e.target.value;
      DOM.btnClearSearch.style.display = e.target.value ? "block" : "none";
      renderTable();
    });
    DOM.btnClearSearch.addEventListener("click", clearSearch);
    DOM.filterCategory.addEventListener("change", (e) => {
      state.filter.category = e.target.value;
      renderTable();
    });
    DOM.filterStatus.addEventListener("change", (e) => {
      state.filter.status = e.target.value;
      renderTable();
    });
    DOM.sortBy.addEventListener("change", (e) => {
      state.filter.sortBy = e.target.value;
      renderTable();
    });
    DOM.btnResetFilters.addEventListener("click", resetFilters);
    DOM.btnEmptyClear.addEventListener("click", resetFilters);
    DOM.btnResetSampleData.addEventListener("click", resetSampleData);

    // Modal Form Submissions
    DOM.btnCloseModalForm.addEventListener("click", () => closeModal(DOM.modalItemForm));
    DOM.btnCancelForm.addEventListener("click", () => closeModal(DOM.modalItemForm));
    DOM.itemForm.addEventListener("submit", handleFormSubmit);

    // Modal Delete Submissions
    DOM.btnCloseDeleteModal.addEventListener("click", () => closeModal(DOM.modalDeleteConfirm));
    DOM.btnCancelDelete.addEventListener("click", () => closeModal(DOM.modalDeleteConfirm));
    DOM.btnConfirmDelete.addEventListener("click", confirmDeleteItem);

    // Clear Logs
    DOM.btnClearLogs.addEventListener("click", () => {
      state.logs = [];
      try {
        localStorage.removeItem(STORAGE_KEYS.LOGS);
      } catch (e) {}
      renderActivityLogs();
      announce("Activity audit log cleared.");
    });
  }

  // --------------------------------------------------------------------------
  // Application Bootstrap
  // --------------------------------------------------------------------------
  function init() {
    loadA11yPreferences();
    loadInventoryData();
    initEvents();
    initKeyboardShortcuts();
    renderTable();
    renderActivityLogs();
  }

  // Run on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
