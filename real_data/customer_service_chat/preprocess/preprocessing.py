import pandas as pd
import os

# Get the path to the current file (preprocessing.py)
BASE_DIR = os.path.dirname(__file__)
# Load the raw dataset
RAW_PATH = os.path.join(BASE_DIR,"..", "raw", "chat_Data.xlsx")

print("Looking for the file at:", os.path.abspath(RAW_PATH))

# Read the CSV file using pandas
df = pd.read_excel(RAW_PATH)

# Print the shape awnd column names
print("✅ Dataset loaded.")
print(f"Shape: {df.shape}")
print("Columns:", df.columns.tolist())

# Display the first few rows to understand the structure
print("\n🔍 Sample data:")
print(df.head(5))
