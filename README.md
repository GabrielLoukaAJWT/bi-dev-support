# Oracle SQL Query Performance Analyzer

This project is a Python-based tool that connects to an Oracle database using the Oracle Instant Client (thick mode), executes SQL queries, captures execution time, and optionally analyzes execution plans.

> Ideal for developers, analysts, and students who want to understand and compare SQL performance inside Oracle.

---

## Features

- Allows to run SQL Queries via input
- Shows performace analytics
- Saves query history and performance logs
- Easy-to-use and extendable structure

---

## Tech Stack

- Python 3.13
- [`oracledb`](https://python-oracledb.readthedocs.io/en/latest/index.html)
- Oracle Instant Client (for thick mode)
- `matplotlib`, `numpy`

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
                         and put the directory to be used for the connection (See LIB_DIR in constants.py)

### 3. Install packages
Run 'pip install -r requirements.txt' in a virtual environment (create one by running 'pip -m venv myenv')

### 4. How to build
To build the project, run 'pyinstaller main.py --icon=assets/images/icon.ico --noconsole --onedir --name SQL-Analytics-vX.Y.Z'

### 5. Tests and coverage
To get a coverage report and test:
- run 'coverage run --branch --source=src -m pytest tests/<optional specific test file>' in root (also runs tests)
- run 'coverage html -d .\tests\coverage\htmlreport' in root