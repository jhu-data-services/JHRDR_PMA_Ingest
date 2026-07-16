## JHRDR PMA Data Ingest

#### November 2024

This repository contains a set of python scripts used to transfer data from PMA to JHRDR, and documentation of how the work was done. 

PMA (Performance Monitoring for Accountability) is an research group at the School of Public Health. They have a client account from DataCite and can mint their own DOIs. Their funding with the Gates Foundation is ended is in 2024, so they asked us to transfer the datasets to be hosted on JHRDR. These datasets already have DOIs and researchers want to keep the same DOIs. They also have landing pages with metadata and minimal metadata in DataCite.

### Approach 

We utilized the [Import CSV to Dataverse](https://pydataverse.readthedocs.io/en/latest/user/advanced-usage.html) functionality of the python package `pydataverse`. 

We adapted the pydataverse CSV templates to be user-friendly to PMA, and then wrote python scripts to transform the metadata we received from them into the CSV template format and to automate the upload of the metadata and files into JHRDR. 

### Files in this Repository
- `PMA_metadata_template.xlsx`: the template we provided to PMA to fill out with metadata about the collections, datasets, and files to be uploaded
- `fill_csv.py` - Python script to transform the metadata recieved from PMA into the pydataverse csv template for batch dataset upload - for the PMA datasets.
- `ingest_csv.py` - Python script to upload files to the PMA datasets.
- `find_file_mismatches.py` - identifies files that are listed in the metadata sheet but not found in the file directory. 

### Files not in this Repository

For licensing reasons, the actual data files uploaded to JHRDR are not included in this repository. 

### How to use/adapt this code

The workflow is as follows:
- Insert files to be uploaded into the same directory as `PMA_metadata_template.xlsx`. The files for each dataset should be in their own folder, with the name of that folder indicated in the "Folder Name" column of the files sheet of `PMA_metadata_template.xlsx`. (as described in the instructions sheet).
- Run `fill_csv.py` to transform metadata collected in `PMA_metadata_template.xlsx` to the schema required for upload by pydataverse. This will output 2 files: `pma_datasets_toupload.csv` and `pma_files_toupload.csv`.
- *Optional* Run `find_file_mismatches.py` to identify files that are listed in the files metadata csv but not found in the file directory.
- Run `ingest_csv.py`, which reads in `pma_datasets_toupload.csv` and `pma_files_toupload.csv` and creates the datasets and upload their corresponding files to Dataverse. Be sure to change the value for `dv_alias` to the Dataverse you want to upload to.

### Requirements

- `Python 3.11.4`
- `pandas 1.5.3`
- `numpy 1.24.3`
- `json`
- `os`
- `pydataverse 0.3.1`

### Citation

Please cite this material as:
Johns Hopkins University Data Services. JHRDR_PMA_Ingest. https://github.com/jhu-data-services/JHRDR_PMA_Ingest

