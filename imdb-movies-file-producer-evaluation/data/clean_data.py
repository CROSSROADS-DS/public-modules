import numpy as np
import pandas as pd

df = pd.read_csv("./movies.csv").dropna(axis=0)

if "released" not in df:
    print("Data has already been cleaned by this script")
    exit(0)

released_terms = df["released"].str.split(" ", expand=True)[[0, 1, 2]]
released_terms[1] = pd.to_numeric(released_terms[1].str.removesuffix(','), errors="coerce")
released_terms = released_terms.dropna(axis=0)

df["release_month"] = released_terms[0]
df["release_day"] = released_terms[1].astype(np.int64)

df = df.drop(columns="released")

df = df[df["year"] != 2020]

df['release_month'] = df['release_month'].map({
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
})

df.to_csv("./movies.csv", index=False, index_label=None)