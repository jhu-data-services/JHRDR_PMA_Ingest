import os
import pandas as pd

# find files that don't match between the spreadsheet and the file system

# replace with the appropriate dataset for the collection
files_toupload = pd.read_csv('pma_files_toupload.csv')

for index, row in files_toupload.iterrows():
	for root, dirs, files in os.walk(row["folder"]):
		if row["org.filename"] not in files:
			print(os.path.join(root, row["org.filename"]))