import glob
import pandas as pd

# Week 1 Aggregation Script
# Combines monthly sold datasets (Jan 2024 → Mar 2026)
# Validates row counts and filters Residential properties


# Step 1: Verify files  & sorted by monthly properly
files = sorted(glob.glob("../raw/CRMLSSold*.csv"))
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
sold_res.to_csv("../output/sold_combined.csv", index=False)
print("\nSaved: sold_combined.csv")



'''
# In terminal: python sold_aggregation.py 
result:

Number of files: 27
First 5 files: ['raw/CRMLSSold202401.csv', 'raw/CRMLSSold202402.csv', 'raw/CRMLSSold202403.csv', 'raw/CRMLSSold202404.csv', 'raw/CRMLSSold202405.csv']

Sample data:
              BuyerAgentAOR  ... OriginatingSystemSubName
0               Mlslistings  ...               CRMLS_MLSL
1                HighDesert  ...                CRMLS_CRM
2              OrangeCounty  ...                CRMLS_CRM
3             InlandValleys  ...                CRMLS_CRM
4  SouthwestRiversideCounty  ...                CRMLS_CRM

[5 rows x 80 columns]
Rows in first file: 17976

=== Individual File Row Counts ===
raw/CRMLSSold202401.csv 17976
raw/CRMLSSold202402.csv 19925
raw/CRMLSSold202403.csv 23276
raw/CRMLSSold202404.csv 24640
raw/CRMLSSold202405.csv 26487
raw/CRMLSSold202406.csv 24328
raw/CRMLSSold202407.csv 26240
raw/CRMLSSold202408.csv 24558

raw/CRMLSSold202409.csv 21267
raw/CRMLSSold202410.csv 23274
raw/CRMLSSold202411.csv 20279
raw/CRMLSSold202412.csv 20241
raw/CRMLSSold202501.csv 18738
raw/CRMLSSold202502.csv 18702
raw/CRMLSSold202503.csv 21445
raw/CRMLSSold202504.csv 23262
raw/CRMLSSold202505.csv 23154
raw/CRMLSSold202506.csv 22883
raw/CRMLSSold202507.csv 23646
raw/CRMLSSold202508.csv 22972
raw/CRMLSSold202509.csv 22443
raw/CRMLSSold202510.csv 23233
raw/CRMLSSold202511.csv 19088
raw/CRMLSSold202512.csv 20538
raw/CRMLSSold202601.csv 16487
raw/CRMLSSold202602.csv 19106
raw/CRMLSSold202603.csv 23545

Total rows before concat: 591733
Total rows after concat: 591733

=== PropertyType BEFORE filter ===
PropertyType
Residential            397603
ResidentialLease       135617
Land                    19345
ManufacturedInPark      16082
ResidentialIncome       15865
CommercialSale           3714
CommercialLease          3104
BusinessOpportunity       403
Name: count, dtype: int64

Rows before filter: 591733
Rows after filter: 397603
Rows removed: 194130

=== PropertyType AFTER filter ===
PropertyType
Residential    397603
Name: count, dtype: int64

Saved: sold_combined_residential.csv
'''
