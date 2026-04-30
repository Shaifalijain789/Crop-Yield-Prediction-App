import pandas as pd
import os

# ================== CONFIG ==================
processed_folder = "processed_crop_data"
output_file = "all_states_crop_data.csv"

# ================== READ ALL PROCESSED FILES ==================
files = [
    f for f in os.listdir(processed_folder)
    if f.endswith(".csv")
]

if not files:
    print(" No processed CSV files found.")
    exit()

df_list = []

for file in files:
    file_path = os.path.join(processed_folder, file)
    df = pd.read_csv(file_path)
    df_list.append(df)
    print(f"Loaded: {file}")

# ================== COMBINE ==================
df_combined = pd.concat(df_list, ignore_index=True)

# ================== SAVE ==================
df_combined.to_csv(output_file, index=False)

print(f"\n Combined file saved as: {output_file}")
print(f" Total records: {len(df_combined)}")
