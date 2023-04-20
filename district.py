import pandas as pd

df = pd.read_excel("data/London postcode districts.xlsx")
print(df["Postcode district"].values)
postcode = df["Postcode district"].values
borough = df.Borough.values
