import glob
import pandas as pd

# Week 1 Aggregation Script
# Combines monthly sold datasets (Jan 2024 → Mar 2026)
# Validates row counts and filters Residential properties


# Step 1: Verify files  & sorted by monthly properly
files = sorted(glob.glob("raw/CRMLSSold*.csv"))
print("Number of files:", len(files))
print("First 5 files:", files[:5])


# Step 2: Load ONE file to test
df = pd.read_csv(files[0], low_memory=False)
print("\nSample data:")
print(df.head())
print("Rows in first file:", len(df))


# step 3: loop thru all files
dfs = []
total_rows = 0

print("\n=== Individual File Row Counts ===")
for file in files:
    df = pd.read_csv(file, low_memory=False)
    
    print(file, len(df))   # validation
    
    total_rows += len(df)
    dfs.append(df)

print("\nTotal rows before concat:", total_rows)


# step 4: combine everything
sold_all = pd.concat(dfs, ignore_index=True)
print("Total rows after concat:", len(sold_all))

# step 5: validate append
assert total_rows == len(sold_all), "Row count mismatch!"

# step 6: PropertyType BEFORE filter
print("\n=== PropertyType BEFORE filter ===")
print(sold_all['PropertyType'].value_counts())

# step 7: apply filter
sold_res = sold_all[sold_all['PropertyType'] == 'Residential']

# step 8: validation AFTER filter 
print("\nRows before filter:", len(sold_all))
print("Rows after filter:", len(sold_res))
print("Rows removed:", len(sold_all) - len(sold_res))

print("\n=== PropertyType AFTER filter ===")
print(sold_res['PropertyType'].value_counts())

# save output
sold_res.to_csv("sold_combined_residential.csv", index=False)
print("\nSaved: sold_combined_residential.csv")

