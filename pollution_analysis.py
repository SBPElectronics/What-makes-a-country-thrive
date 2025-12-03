import pandas as pd
import matplotlib.pyplot as plt


# Load CSV
df = pd.read_csv("pollution.csv")

# Select all AQI columns automatically
aqi_cols = [col for col in df.columns if "AQI" in col]

# Convert AQI columns to numeric, forcing errors to NaN
for col in aqi_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Now compute one overall AQI per row (average across all AQI columns, ignoring NaN)
df['AQI_overall'] = df[aqi_cols].mean(axis=1)

# Group by country and compute average AQI
df_country_avg = df.groupby("Country")['AQI_overall'].mean().reset_index()
df_country_avg.rename(columns={'AQI_overall': 'Average_AQI'}, inplace=True)

# Show results
print(df_country_avg)

# Sort countries from cleanest (lowest AQI) to dirtiest (highest AQI)
df_country_avg_sorted = df_country_avg.sort_values(by='Average_AQI')

# Display the table
print(df_country_avg_sorted)


plt.figure(figsize=(15,6))
plt.bar(df_country_avg_sorted['Country'], df_country_avg_sorted['Average_AQI'], color='skyblue')
plt.xticks(rotation=90)
plt.ylabel("Average AQI")
plt.title("Average AQI by Country")
plt.tight_layout()
plt.show()





