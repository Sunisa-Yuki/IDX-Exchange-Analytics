import glob
import pandas as pd
import os
print(os.listdir("../raw"))

# Week 1 Aggregation Script (Listings)
# Combines monthly listing datasets (Jan 2024 → Mar 2026)
# Validates row counts and filters Residential properties



# Step 1: Verify files
# files = sorted(glob.glob("../raw/CRMLSListing*.csv"))
print(os.listdir("raw"))
files = sorted(glob.glob("raw/*Listing*.csv"))

print("Number of files:", len(files))
print("First 5 files:", files[:5])

# Step 2: Load one file (sanity check)
df = pd.read_csv(files[0], low_memory=False)
print("\nSample data:")
print(df.head())
print("Rows in first file:", len(df))

# Step 3: Loop through all files
dfs = []
total_rows = 0

if len(files) == 0:
    raise ValueError("No files found. Check your raw folder or filename pattern.")
print("\n=== Individual File Row Counts ===")

for file in files:
    try:
        df = pd.read_csv(file, low_memory=False)
        
        print(file, len(df))
        
        total_rows += len(df)
        dfs.append(df)
    
    except Exception as e:
        print(f"ERROR reading {file}: {e}")

# Step 4: Combine datasets
listings_all = pd.concat(dfs, ignore_index=True)
print("Total rows after concat:", len(listings_all))

# Step 5: Validate append
assert total_rows == len(listings_all), "Row count mismatch!"

# Step 6: PropertyType BEFORE filter
print("\n=== PropertyType BEFORE filter ===")
print(listings_all['PropertyType'].value_counts())

# Step 7: Filter Residential
listings_res = listings_all[listings_all['PropertyType'] == 'Residential']

# Step 8: Validation AFTER filter
print("\nRows before filter:", len(listings_all))
print("Rows after filter:", len(listings_res))
print("Rows removed:", len(listings_all) - len(listings_res))

print("\n=== PropertyType AFTER filter ===")
print(listings_res['PropertyType'].value_counts())

# Step 9: Save output
listings_res.to_csv("../output/listings_combined.csv", index=False)
print("\nSaved: listings_combined.csv")



