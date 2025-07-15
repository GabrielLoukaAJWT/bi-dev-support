# Oracle SQL Query Performance Analyzer

This project is a Python-based tool that connects to an Oracle database using the Oracle Instant Client (thick mode), executes SQL queries, captures execution time, and optionally analyzes execution plans.

> Ideal for developers, analysts, and students who want to understand and compare SQL performance inside Oracle.

---

## Features

- Connects securely to Oracle using `oracledb` (thick mode)
- Executes arbitrary SQL queries from `.sql` files or inline input
- Measures execution time (runtime benchmarking)
- Saves query history and performance logs (CSV or SQLite)
- Easy-to-use and extendable structure

---

## Tech Stack

- Python 3.13 64-bit
- [`oracledb`](https://python-oracledb.readthedocs.io/en/latest/index.html)
- Oracle Instant Client (for thick mode)
- `getpass` for secure credential input
- `pandas` and `matplotlib` (optional for analysis/plotting)
- `sqlite3` (optional for logging history)

---

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/GabrielLoukaAJWT/bi-dev-support.git<br>
cd bi-dev-support

### 2. Install Oracle Instant Client

The current oracledb library runs on thin mode, which supports passwords verifiers 11G and later,
but the current Oracle account was created with 10G.
    - Option 1 : change password for the database user
    - Option 2 : Install Oracle Instant Client (https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html)
                         and put the directory to be used for the connection (See LIB_DIR at constants.py)
