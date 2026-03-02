from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.schema_generator import initialize_database

if __name__ == "__main__":
    initialize_database()
    print("Database initialized.")
