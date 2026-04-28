import pandas as pd

# Load datasets
sold = pd.read_csv("../output/sold_combined_residential.csv")
listings = pd.read_csv("../output/listings_combined_residential.csv")

print("========= BASIC INFO =========")
print("Sold shape:", sold.shape)
print("Listings shape:", listings.shape)

print("\n========= COLUMNS =========")
print(sold.columns)

print("\n========= DATA TYPES =========")
print(sold.dtypes)

# -------------------------- Missing Values ---------------------------- 
print("\n========= MISSING VALUES =========")

missing = sold.isnull().sum()
missing_percent = (missing / len(sold)) * 100

missing_df = pd.DataFrame({
    "missing_count": missing,
    "missing_percent": missing_percent
})

print(missing_df.sort_values(by="missing_percent", ascending=False).head(20))

# -------------------------- PropertyType Check ---------------------------- 
print("\n========= PROPERTY TYPE CHECK =========")
print(sold['PropertyType'].value_counts())


# ------------------------- Numeric Summary ---------------------------- 
print("\n========= NUMERIC SUMMARY =========")

cols = ["ClosePrice", "LivingArea", "DaysOnMarket"]

for col in cols:
    print(f"\n--- {col} ---")
    print(sold[col].describe())

# ------------------------- Mortgage rate merge ---------------------------- 

print("\n========= FETCHING MORTGAGE DATA =========")

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

# Convert to monthly
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed']
    .mean()
    .reset_index()
)

# Create keys
sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')
listings['year_month'] = pd.to_datetime(listings['ListingContractDate']).dt.to_period('M')

# Merge
sold = sold.merge(mortgage_monthly, on='year_month', how='left')
listings = listings.merge(mortgage_monthly, on='year_month', how='left')

# Validate
print("\n========= MERGE VALIDATION =========")
print("Sold null rates:", sold['rate_30yr_fixed'].isnull().sum())
print("Listings null rates:", listings['rate_30yr_fixed'].isnull().sum())

# ------------------------- Save output ---------------------------- 
sold.to_csv("../output/sold_with_rates.csv", index=False)
listings.to_csv("../output/listings_with_rates.csv", index=False)

print("\nSaved enriched datasets.")