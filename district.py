import pandas as pd

df = pd.read_excel("./data/London postcode districts.xlsx")

# check if there are missing values
#print(df.Borough.isnull().sum())
#print(df["Postcode district"].isnull().sum())

# create list of postcode and district names
postcode = df["Postcode district"].values
borough = df.Borough.values

# create batches of postcodes and district names
postcode_batch2, borough_batch2 = postcode[35:65], borough[35:65]
postcode_batch3, borough_batch3 = postcode[65:95], borough[65:95]
postcode_batch4, borough_batch4 = postcode[95:125], borough[95:125]
postcode_batch5, borough_batch5 = postcode[125:155], borough[125:155]
postcode_batch6, borough_batch6 = postcode[155:185], borough[155:185]
postcode_batch7, borough_batch7 = postcode[185:215], borough[185:215]
postcode_batch8, borough_batch8 = postcode[215:245], borough[215:245]
postcode_batch9, borough_batch9 = postcode[245:], borough[245:]
