# Apex Regional Logistics & Revenue Audit Engine

A modular Python application that automates sales auditing, tiered commission calculation, and warehouse dispatch for a fictional multi-store distribution company, **Apex Freight & Supply**.

Built as a course project for a Python programming class (Gaddis, *Starting Out with Python*, Chapters 1–14). The project was delivered in 9 phases, with each phase adding a new capability without breaking the ones before it.

![Dispatch Dashboard](screenshots/dashboard.png)

---

## Features

| Phase | Feature | What it does |
|---|---|---|
| I | **Console audit core** | Collects store/department sales with input validation, flags frozen ledger entries, calculates tiered commissions, and prints a formatted audit report and rack grid |
| II | **Ledger files & exceptions** | Writes every sale to a CSV-style ledger, verifies totals, archives the ledger, and handles bad data without crashing |
| III | **Store collections & charts** | Ranks and analyzes store sales with lists/tuples, and plots line, bar, and pie charts with matplotlib |
| IV | **String processing** | Cleans messy manifest lines and validates product SKUs (e.g. `APX-1234-NW`) |
| V | **Directories, sets & snapshots** | Department lookup tables (dictionaries), carrier ZIP code coverage comparisons (sets), and pickled audit snapshots |
| VI | **Fleet object model** | `FleetVehicle` class with `BoxTruck` and `CargoVan` subclasses, using inheritance, method overriding, and hidden attributes |
| VII | **Recursion** | Recursive sales totals, batch-size calculation (GCD), and dispatch countdowns |
| VIII | **Dispatch dashboard (GUI)** | Tkinter window with a mileage payout calculator, tier/surcharge options, a scrollable store list, and a canvas-drawn warehouse rack |
| IX | **SQLite database** | Stores and Departments tables with primary/foreign keys, plus parameterized inserts, filtered queries, aggregations, updates, deletes, and a two-table join report |

---

## Tech Stack

- **Python 3**
- **SQLite** (`sqlite3`)
- **Tkinter** (GUI)
- **Matplotlib** (charts)
- Standard library: `random`, `math`, `os`, `pickle`

---

## Project Structure

```
apex-audit-engine/
├── apex_audit.py       # Main program: Phases I–V, VII, and main()
├── apex_geometry.py    # Math helpers (distance, angles, growth) used by Phase I
├── apex_models.py      # Phase VI: FleetVehicle, BoxTruck, CargoVan classes
├── apex_dashboard.py   # Phase VIII: Tkinter dispatch dashboard
├── apex_database.py    # Phase IX: SQLite schema, queries, and reports
└── README.md
```

`apex_audit.py` imports the other four modules and runs everything from `main()`.

---

## How to Run

1. **Install Python 3** (3.10 or newer recommended).
2. **Install matplotlib:**
```
   pip install matplotlib
```
3. **Keep all 5 `.py` files in the same folder**, then run:
```
   python apex_audit.py
```

### Sample input

| Prompt | Example |
|---|---|
| Number of stores | `3` |
| Number of departments | `2` |
| Tier code | `A` |
| Regional target | `0` (uses the default $50,000 quota) |
| Store sales | `500`, `-999`, `1200`, `300`, `800`, `-50` |
| Carton count | `100` |

`-999` flags a frozen department ledger, and negative sales are reset to 0.

### What happens

1. The audit report prints (total sales, commission, formatted figures).
2. The ledger is written, verified, and displayed.
3. Three chart windows open one at a time (close each to continue).
4. Department directory, fleet settlement, and database query results print.
5. The rack grid prints, then the **Dispatch Dashboard** opens.

The program creates these files while running: `ledger_archive.txt`, `store_sales.txt`, `audit_snapshot.dat`, and `apex.db`.

---

## Sample Output

```
============================================================
                   Regional Audit Report
                   Commission rate : 15%
============================================================
Total Sales:                2,800.00
Commission earned:    $        420.00
Effective rate:       15.0%
Average per store: 933.33
...
Store 1      Dept 1       500.00
Store 2      Dept 1     1,500.00
Store 3      Dept 1       800.00
```

---

## Concepts Practiced

- Functions, parameters, multiple return values, and a `main()` that only orchestrates
- Input validation with loops and `try / except`
- File I/O, exception handling, and file archiving
- Lists, tuples, dictionaries, sets, and comprehensions
- String methods for cleaning and validating data
- Object-oriented programming: classes, inheritance, overriding, encapsulation
- Recursion
- GUI programming with Tkinter
- SQL with SQLite: schema design, keys, parameterized queries, aggregates, and joins

---

## Darrious Bedford

**Darrious Bedford**
Information Systems, Texas State University
[GitHub](https://github.com/DarriousBedford)
