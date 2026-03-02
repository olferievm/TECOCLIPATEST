# Local Clinical Data Collection Server

A lightweight local web app for collecting structured clinical data from `data/generated_schema.csv`.

## Features

- CSV-driven SQLite schema generation from repository metadata
- Session-based authentication with bcrypt password hashing
- Multi-step patient entry wizard with lookup-backed dropdown fields
- Searchable + sortable dashboard across all schema columns
- Role-based CSV and XLSX export (`admin` and `registered_user`)

## Quick start (macOS / Windows)

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
python scripts/init_database.py
python run.py
```

Open:

- `http://localhost:8000` (local machine)
- `http://<your-lan-ip>:8000` (same network)

Default admin user:

- username: `admin`
- password: `admin123`

## Configuration

Set optional environment variables for cross-platform local deployment:

- `HOST` (default `0.0.0.0`)
- `PORT` (default `8000`)
- `APP_SECRET_KEY`
- `SESSION_MAX_AGE_SECONDS`
- `DEFAULT_ADMIN_USERNAME`
- `DEFAULT_ADMIN_PASSWORD`

## Notes

- Database file: `data/database.sqlite`
- Tables are auto-generated from `data/generated_schema.csv`.
