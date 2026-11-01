"""
================================================================================
BBAT104: FUNDAMENTALS OF TQM - COURSE PROJECT 2026-27
STUDENT NAME : RAHUL MEHRA
DEPARTMENT   : CSE, AIML SECB
BASELINE SYS : INVENTORY MANAGEMENT SYSTEM (DIGIT 3: STOCKOUTS & TURNOVER)
QUALITY GOAL : Q12: IMPROVE ACCESSIBILITY
               1. HIGH CONTRAST MODE
               2. DYNAMIC FONT RESIZING
               3. FULL KEYBOARD NAVIGATION
               4. DARK / LIGHT THEME ENGINE
               5. MINIMALIST COGNITIVE LAYOUT
================================================================================
"""

import sys
import os
import tkinter as tk
from database import Database, DEFAULT_DB_FILE
from ui.app_window import InventoryAppWindow


def main():
    """Application entry point."""
    print("=" * 75)
    print("BBAT104: TQM Project - CSE AIML Hardware Inventory Management System")
    print("Student: Rahul Mehra | Branch: CSE AIML (Sec B) | Goal: Q12 Accessibility")
    print(f"Database: {DEFAULT_DB_FILE}")
    print("=" * 75)

    # Initialize SQLite Database
    db = Database(DEFAULT_DB_FILE)

    # Initialize Tkinter GUI
    root = tk.Tk()

    # Apply application window
    app = InventoryAppWindow(root, db)

    # Enter GUI Event Loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
