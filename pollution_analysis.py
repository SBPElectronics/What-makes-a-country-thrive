import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pollution.csv")


# 2. Identify AQI columns
aqi_cols = [col for col in df.columns if "AQI" in col]


df[aqi_cols] = df[aqi_cols].apply(pd.to_numeric, errors="coerce")


# 4. Average AQI per row (for all city measurements)
df["AQI_overall"] = df[aqi_cols].mean(axis=1)

# 5. Average AQI per country

df_country_avg = (
    df.groupby("Country")["AQI_overall"]
    .mean()
    .reset_index()
    .rename(columns={"AQI_overall": "Average_AQI"})
)

# 6. Sort countries from cleanest ➝ dirtiest
df_country_avg_sorted = df_country_avg.sort_values("Average_AQI")

# 7. Display summary table
print(df_country_avg_sorted)

plt.figure(figsize=(14, 7))
plt.barh(df_country_avg_sorted["Country"], df_country_avg_sorted["Average_AQI"])
plt.xlabel("Average AQI")
plt.title("Average AQI by Country (Cleanest → Dirtiest)")
plt.tight_layout()
plt.show()



