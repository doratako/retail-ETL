import os
import glob
import pandas as pd

# get the latest file from the source folder
folder_path = ".\\customer_source"
files = glob.glob(f"{folder_path}/*.csv")
customer_latest_file = max(files, key=os.path.getctime)


customer_df = pd.read_csv(customer_latest_file)

if __name__ == "__main__":
    print(customer_df.info())

    customer_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    print(customer_df.isna().any())

    print(customer_df[customer_df.duplicated(keep="first")])
    customer_df.drop_duplicates(keep="first", inplace=True)

    print(customer_df.head())





