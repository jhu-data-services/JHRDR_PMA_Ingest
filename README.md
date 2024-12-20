## JHRDR PMA Data Ingest

#### November 2024

This repository contains a set of python scripts used to transfer data from PMA to JHRDR, and documentation of how the work was done. 

PMA (Performance Monitoring for Accountability) is an research group at the School of Public Health. They have a client account from DataCite and can mint their own DOIs. Their funding with the Gates Foundation is ended is in 2024, so they asked us to transfer the datasets to be hosted on JHRDR. These datasets already have DOIs and researchers want to keep the same DOIs. They also have landing pages with metadata and minimal metadata in DataCite.

### Approach 

We utilized the [Import CSV to Dataverse](https://pydataverse.readthedocs.io/en/latest/user/advanced-usage.html) functionality of the python package `pydataverse`. 

We adapted the pydataverse CSV templates to be user-friendly to PMA, and then wrote python scripts to transform the metadata we received from them into the CSV template format and to automate the upload of the metadata and files into JHRDR.

### Files in this Repository
- `PMA_metadata_template.xlsx`: the template we provided to PMA to fill out with metadata about the collections, datasets, and files to be uploaded
- `PMAET` - scripts to upload data to the PMA Ethiopia Collection
	- `fill_pmaet_codebook_csv.py` - Python script to transform the metadata recieved from PMA into the pydataverse csv template for batch dataset upload - for the PMA Ethiopia codebooks.
	- `ingest_pmaet_codebook.py` - Python script to upload files to the PMA Ethiopia codebook datasets.
	- `fill_pmaet_dataset_csv.py` - Python script to transform the metadata recieved from PMA into the pydataverse csv template for batch dataset upload - for the PMA Ethiopia datasets.
	- `ingest_pmaet.py` - Python script to upload files to the PMA Ethiopia datasets.
- `PMA2020` - scripts to upload data to the PMA2020 Collection
	- `fill_pma2020_codebook_csv.py` - Python script to transform the metadata recieved from PMA into the pydataverse csv template for batch dataset upload - for the PMA 2020 codebooks.
	- `ingest_pma2020_codebook.py` - Python script to upload files to the PMA 2020 codebook datasets.
	- `fill_pma2020_dataset_csv.py` - Python script to transform the metadata recieved from PMA into the pydataverse csv template for batch dataset upload - for the PMA 2020 datasets.
	- `ingest_pma2020.py` - Python script to upload files to the PMA 2020 datasets.
- `PMA` - scripts to upload data to the PMA Collection
	- `fill_pma_codebook_csv.py` - Python script to transform the metadata recieved from PMA into the pydataverse csv template for batch dataset upload - for the PMA codebooks.
	- `ingest_pma_codebook.py` - Python script to upload files to the PMA codebook datasets.
	- `fill_pma_dataset_csv.py` - Python script to transform the metadata recieved from PMA into the pydataverse csv template for batch dataset upload - for the PMA datasets.
	- `ingest_pma.py` - Python script to upload files to the PMA datasets.
- `find_file_mismatches.py` - identifies files that are listed in the metadata sheet but not found in the file directory. This script can be placed in each subfolder to be run for each collection.

### Files not in this Repository

For licensing reasons, the actual data files uploaded to JHRDR are not included in this repository. 

### Requirements

- `Python 3.11.4`
- `pandas 1.5.3`
- `numpy 1.24.3`
- `json`
- `os`
- `pydataverse 0.3.1`

### Data Migration Procedure

Below are the steps taken to batch upload the PMA data into JHRDR: 
- Contact DataCite to transfer DOIs from the PMA account to our GDCC account (this enabled us to publish the datasets in our repository and maintain the same DOIs). 
- Send metadata template to PMA and receive completed template.
- Remove the first column and save the datasets and files sheets as csvs.
- Break up the datasets and files csvs into separate csvs for each dataverses - we could have done this all in one metadata sheet and generalized the code more, but for testing purposes we broke it up by dataverse. Make sure the csvs are saved as CSV (UTF-8 encoded) in order to preserve the non-English characters in the metadata. We also separated the codebook dataset and file metadata for each dataverse - again, for testing purposes and because the other datasets link to the codebooks.
- Into the same directory as the csvs, insert the files from PMA (in folders as described in the instructions in the metadata template)
- Create dataverses in the Dataverse instance (as described in the collections tab of the metadata template) and insert the dataverse id into the `dv_alias` variable in the `ingest_` Python scripts.
- To create datasets and upload files for a given collection, run the scripts in each subfolder in a bash shell (i.e. Terminal, Anaconda Prompt, Git Bash) in the following order:
	- `python fill_[collectionname]_codebook_csv.py` 
	- `python ingest_[collectionname]_codebook.py`
	- `python fill_[collectionname]_dataset_csv.py`
	- `pythong find_file_mismatches.py` - this script checks for any files that are listed in the metadata sheet but not found in the directory.
	- `python ingest_[collectionname].py`

