import os
import glob
import pandas as pd

# get the latest file from the source folder
folder_path = ".\\transaction_source"
files = glob.glob(f"{folder_path}/*.csv")
transaction_latest_file = max(files, key=os.path.getctime)

retail_df = pd.read_csv(transaction_latest_file)

# removing leading and trailing whitespace from strings, if there are any
retail_df = retail_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

retail_df.dropna(subset="Customer ID", inplace=True)

# removing rows with empty Customer ID removes empty values from the Description
retail_df.isnull().any()

retail_df.drop_duplicates(keep="first", inplace=True)

retail_df["Customer ID"] = retail_df["Customer ID"].astype(int)

retail_df.rename(columns={"Customer ID": "Customer_ID", "Price": "UnitPrice", "Invoice": "Invoice_ID"}, inplace=True)


if __name__ == "__main__":
    print(retail_df.isna().any())
    print(retail_df.loc[retail_df.isna().any(axis=1)])
    print(retail_df[retail_df.duplicated(keep="first")])
    print(retail_df.info())
    print(retail_df.info())