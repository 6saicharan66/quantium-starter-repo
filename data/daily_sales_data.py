import dask.dataframe as dd
import pandas as pd

ddf = dd.read_csv(f"C:\\users\\Sushmitha\\Desktop\\MY_SPACE\\FORGE TASKS\\quantium-starter-repo\\data/*.csv")
df = ddf.compute()
df["sales"] = df["price"].str.replace('$', ' ').astype('float') * df["quantity"]
product = "pink morsel"
df = df.loc[df["product"] == product]
df = df[["sales", "date", "region", ]]
print(df)
df.to_csv('pink_morsel_sales.csv', index=False)
