import os
import zipfile
import pandas as pd

input_dir = "files/input"

months_count = {}
for file in sorted(os.listdir(input_dir)):
    if file.endswith(".zip"):
        zip_path = os.path.join(input_dir, file)
        print(f"Processing {file}...")
        with zipfile.ZipFile(zip_path) as z:
            csv_name = z.namelist()[0]
            df = pd.read_csv(z.open(csv_name))
            for month in df['month'].unique():
                months_count[month] = months_count.get(month, 0) + len(df[df['month'] == month])
                
print('\nMonths found:', sorted(months_count.keys()))
for month, count in sorted(months_count.items()):
    print(f"  {month}: {count}")
    
# Check specifically for July data
print("\n--- Checking for July data ---")
for file in sorted(os.listdir(input_dir)):
    if file.endswith(".zip"):
        zip_path = os.path.join(input_dir, file)
        with zipfile.ZipFile(zip_path) as z:
            csv_name = z.namelist()[0]
            df = pd.read_csv(z.open(csv_name))
            july_data = df[df['month'] == 'july']
            if len(july_data) > 0:
                print(f"{file}: {len(july_data)} July records")
                july_19 = july_data[july_data['day'] == 19]
                if len(july_19) > 0:
                    print(f"  - {len(july_19)} records with day=19")
