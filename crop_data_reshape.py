import pandas as pd
import os
import re

# ================== CONFIG ==================
input_folder = "crop_dataset_csv"
output_folder = "processed_crop_data"

os.makedirs(output_folder, exist_ok=True)

# ================== UTILITY FUNCTIONS ==================
def melt_and_extract(df, pattern, value_name, id_vars):
    subset_cols = [col for col in df.columns if pattern in col]

    df_melted = df[id_vars + subset_cols].melt(
        id_vars=id_vars,
        value_vars=subset_cols,
        var_name="Metric_Year",
        value_name=value_name
    )

    df_melted["Year"] = df_melted["Metric_Year"].str.extract(r"(\d{4}-\d{4})")
    df_melted.drop(columns=["Metric_Year"], inplace=True)

    return df_melted


def process_file(input_file_path, output_file_path, state_name):
    df_raw = pd.read_csv(input_file_path, header=None, skiprows=4)

    # ================== DYNAMIC COLUMN HANDLING ==================
    total_cols = df_raw.shape[1]
    metric_cols_count = total_cols - 2  # District + Season

    if metric_cols_count <= 0 or metric_cols_count % 3 != 0:
        print(f"⚠ Skipping {os.path.basename(input_file_path)} (invalid structure)")
        return

    num_years = metric_cols_count // 3
    start_year = 2000

    years = [f"{start_year+i}-{start_year+i+1}" for i in range(num_years)]
    metrics = ["Area", "Production", "Yield"]
    units = ["(Hectare)", "(Tonnes)", "(Ton./Ha.)"]

    new_columns = ["District", "Season"]
    for year in years:
        for metric, unit in zip(metrics, units):
            new_columns.append(f"{metric}_{year}_{unit}")

    df_raw = df_raw.iloc[:, :len(new_columns)]
    df_raw.columns = new_columns

    # ================== CROP EXTRACTION ==================
    df_raw["Crop"] = df_raw.loc[
        df_raw["Season"].isna(), "District"
    ].astype(str).str.extract(r"^\d+\.\s*([^,]+)")

    df_raw["Crop"] = df_raw["Crop"].ffill()

    district_mask = (
        df_raw["District"].astype(str).str.contains(r"^\d+\.\s*\w+", na=False)
        & df_raw["Season"].notna()
    )

    df_final = df_raw[district_mask].copy()
    df_final["District"] = df_final["District"].str.extract(r"^\d+\.\s*([^,]+)")

    metric_cols = [c for c in df_final.columns if c not in ["Crop", "District", "Season"]]
    df_final = df_final[["Crop", "District", "Season"] + metric_cols]

    id_vars = ["Crop", "District", "Season"]

    # ================== MELT DATA ==================
    df_area = melt_and_extract(df_final, "Area_", "Area_(Hectare)", id_vars)
    df_prod = melt_and_extract(df_final, "Production_", "Production_(Tonnes)", id_vars)
    df_yield = melt_and_extract(df_final, "Yield_", "Yield_(Ton./Ha.)", id_vars)

    df_long = (
        df_area
        .merge(df_prod, on=id_vars + ["Year"])
        .merge(df_yield, on=id_vars + ["Year"])
    )

    df_long.insert(0, "State", state_name)
    df_long.to_csv(output_file_path, index=False)

    print(f" Processed: {os.path.basename(output_file_path)}")


# ================== MAIN EXECUTION ==================
files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]

if not files:
    print("No CSV files found in the input folder.")
    exit()

for file in files:
    input_path = os.path.join(input_folder, file)

    # Extract state name from filename
    state_name = re.sub(r"_data\.csv", "", file, flags=re.IGNORECASE)
    state_name = state_name.replace("_", " ")

    output_path = os.path.join(output_folder, f"processed_{file}")

    process_file(input_path, output_path, state_name)

print("\n All files processed successfully!")
