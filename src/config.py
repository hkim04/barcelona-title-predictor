from pathlib import Path

 #find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define where our data is stored
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"