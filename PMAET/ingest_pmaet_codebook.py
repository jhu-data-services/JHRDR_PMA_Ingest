import os
from pyDataverse.utils import read_csv_as_dicts
from pyDataverse.models import Dataverse
from pyDataverse.models import Dataset
from pyDataverse.models import Datafile
from pyDataverse.api import NativeApi

# load metadata for datasets

pma_datasets_csv = "pmaet_codebook_datasets_toupload.csv"
ds_data = read_csv_as_dicts(pma_datasets_csv)

# create a dictionary of datasets

ds_lst = []
for ds in ds_data:
	ds_obj = Dataset()
	ds_obj.set(ds)
	ds_lst.append(ds_obj)

# load metadata for files 

pma_datafiles_csv = "pmaet_codebook_files_toupload.csv"
df_data = read_csv_as_dicts(pma_datafiles_csv)

# create a dictionary of datafiles

df_lst = []
for df in df_data:
	df['restrict'] = False 
	df_obj = Datafile()
	df_obj.set(df)
	df_lst.append(df_obj)

# upload via API

# instantiate API

api = NativeApi("https://archive.data.jhu.edu", "5dc6a0aa-dd4e-4234-82a1-88069b58a6af")

# create and publish dataverses first 


# # # upload datasets

# # NOTE: eventually, instead of hard-coding the pid in create_dataset(), we'll create a mapping between a variable in each ds json object and the doi supplied by PMA

# change the dv_alias to upload to different dataverses - could make this as a field in the spreadsheet

dv_alias = "pmaet"
dataset_id_2_pid = {}
for ds in ds_lst:
	# for some reason we need to manually change the multiple value for productionPlace - but not sure how to do this yet. A problem for future Lubov
	resp = api.create_dataset(dv_alias, ds.json(), pid=ds.get()["org.doi"].replace(" ", ""))
	print(resp.json())
	dataset_id_2_pid[ds.get()["org.dataset_id"]] = resp.json()["data"]["persistentId"]

# # add datafiles to the datasets we created

for df in df_lst:
	pid = dataset_id_2_pid[df.get()["org.dataset_id"]]
	print(pid)
	filename = os.path.join(os.getcwd(), df.get()["org.filename"])
	print(filename)
	df.set({"pid": pid, "filename": filename})
	resp = api.upload_datafile(pid, filename, df.json())
	print(resp.json())

# # publish datasets

# for dataset_id, pid in dataset_id_2_pid.items():
# 	resp = api.publish_dataset(pid, "major")
# 	resp.json()
