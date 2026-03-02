# Project Specification: Local Clinical Data Collection Server

## Overview

Create a lightweight local web application that allows research staff to collect and manage structured patient information through a browser interface. The application must run on both macOS and Windows computers and be accessible only within the local network.

The system will store structured clinical parameters defined in the attached CSV schema (`data_collection_sheet.csv`). Users will enter data through guided forms. Records will be stored in a local database and displayed in a searchable, scrollable table. Authorized users may export records as CSV or XLSX.

The system is intended for small research groups and must prioritize simplicity of deployment.

---

# Functional Requirements

## 1. Deployment

The application must:

* Run on macOS and Windows
* Start with a single command
* Host a local HTTP server
* Accept connections only from the local network

Recommended stack:

Backend:

* Python
* FastAPI or Flask

Database:

* SQLite (default)
* Database stored locally in the project directory

Frontend:

* Simple HTML + JavaScript
* Prefer lightweight frameworks (HTMX or vanilla JS)

---

# System Architecture

## Backend Components

### API Server

Responsibilities:

* Serve the web interface
* Provide REST API endpoints
* Validate incoming data
* Manage authentication
* Query and update database

### Database Layer

Use SQLite.

Tables must be automatically generated from the CSV schema.

Primary entities:

Patients / Records
Lookup tables (restricted categorical values)
Users

---

# Database Schema

## Core Tables

### users

```
id (primary key)
username
password_hash
role
created_at
```

Roles:

* admin
* registered_user
* viewer

Only registered users and admins may export data.

---

### patients

Contains patient identifiers.

```
subject_id (primary key)
group
enrollment_date
sample_collection_date
gender
created_at
```

---

### data tables

The CSV file contains parameters grouped into logical tables.

Detected tables include:

* General
* Medical
* Questionaire
* ACR97

Each table should become a database table with columns derived from the CSV Parameter field.

Example:

```
general_data
medical_data
questionnaire_data
acr97_data
```

Each table must include:

```
id
subject_id (foreign key)
created_at
```

---

### categorical_lookup

Certain parameters have restricted values.

Example:

* gender
* race
* ethnicity
* disease group

These must be stored in lookup tables.

Example structure:

```
lookup_categories
------------------
id
category_name

lookup_values
--------------
id
category_id
value
is_active
```

Administrators can update these lists.

---

# Data Import

The CSV file (`data_collection_sheet.csv`) defines the schema.

Columns:

```
Parameter
Description
Source of data
VariableType
Table
```

Generation rules:

1. Parameter → column name
2. VariableType → column type
3. Table → database table assignment

Suggested mapping:

| VariableType       | SQL Type         |
| ------------------ | ---------------- |
| Date               | DATE             |
| Factor             | TEXT (validated) |
| Numeric            | REAL             |
| Integer            | INTEGER          |
| Unique Primary Key | TEXT             |

---

# User Interface

## Login Page

Fields:

* username
* password

Sessions stored using secure cookies.

---

# Main Dashboard

Features:

* table of all patient records
* filter
* search
* pagination
* scrolling table view

Columns correspond to parameters defined in the CSV.

---

# Patient Entry Wizard

A multi-step form to create a new patient record.

Steps:

1. Patient identifier
2. General information
3. Medical parameters
4. Questionnaire
5. ACR97 criteria

Requirements:

* validation at each step
* ability to save progress
* dropdown menus for categorical variables

---

# Data Table Viewer

The system must display records in a scrollable grid.

Features:

* column sorting
* filtering
* row selection
* record editing

Recommended JS library:

* DataTables
  or
* Tabulator

---

# Export Function

Registered users can export filtered results.

Supported formats:

CSV
XLSX

Export must include:

* selected filters
* visible columns
* full dataset if no filter

Python libraries:

```
pandas
openpyxl
```

---

# Security

Local network access only.

Requirements:

* server binds to local network interface
* optional IP whitelist
* password hashing using bcrypt
* session expiration

---

# Project Structure

```
project_root

app/
    main.py
    config.py
    database.py
    models.py
    schema_generator.py

routers/
    auth.py
    patients.py
    records.py
    export.py

services/
    csv_schema_parser.py
    lookup_manager.py

templates/
    login.html
    dashboard.html
    wizard.html

static/
    css/
    js/

data/
    data_collection_sheet.csv
    database.sqlite

scripts/
    init_database.py

requirements.txt
README.md
```

---

# Key Features to Implement

1. Parse CSV schema automatically
2. Generate database tables
3. Authentication system
4. Patient wizard form
5. Record browser
6. Export functionality
7. Lookup value manager

---

# Example Startup

```
pip install -r requirements.txt
python scripts/init_database.py
python app/main.py
```

Server should start at:

```
http://localhost:8000
```

Accessible within the local network.

---

# Recommended Libraries

Backend

```
fastapi
uvicorn
sqlalchemy
pydantic
bcrypt
pandas
openpyxl
```

Frontend

```
htmx
bootstrap
datatables
```

---

# Future Extensions

Possible upgrades:

* Docker container deployment
* PostgreSQL backend
* audit log tracking
* role-based permissions
* REST API for external tools
* automatic backups
