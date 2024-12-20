import pandas as pd
import json
import numpy as np

# read in data for PMAET codebooks
pma_datasets = pd.read_csv("pma_datasets.csv")
pma_datafiles = pd.read_csv("pma_files.csv")

# remove whitespace and newlines
pma_datasets['dv.title'] = pma_datasets['dv.title'].str.strip()
pma_datasets['org.doi'] = pma_datasets['org.doi'].str.strip()
pma_datasets['dv.author'] = pma_datasets['dv.author'].str.strip()
pma_datasets['dv.dsDescription'] = pma_datasets['dv.dsDescription'].str.replace("\n", "")
pma_datasets['dv.dsDescription'] = pma_datasets['dv.dsDescription'].str.replace("\xa0", "")
pma_datasets['dv.dsDescription'] = pma_datasets['dv.dsDescription'].str.replace('"', '\\"')

pma_datafiles['dv.title'] = pma_datafiles['dv.title'].str.strip()
pma_datafiles['org.filename'] = pma_datafiles['org.filename'].str.strip()

# increment org.dataset_id for every row in the spreadsheet
pma_datasets['org.dataset_id'] = range(1, len(pma_datasets['dv.title'])+1)

# set org.to_upload = TRUE
pma_datasets['org.to_upload'] = True

# turn author column into json - no affiliation
pma_datasets['dv.author'] = pma_datasets['dv.author'].str.split(';')
author_column = []
for index, row in pma_datasets.iterrows():
	author_dict_list = []
	for author in row['dv.author']:
		author_dict_list.append({"authorName": author.strip()})
	author_column.append(author_dict_list)

author_column = [json.dumps(x, ensure_ascii=False) for x in author_column]

pma_datasets['dv.author'] = author_column

# set dv.dsDescription to Description after converting to json format
# [{"dsDescriptionValue": "[[Description from PMA sheet]]"}]
# include links to codebooks as last sentence in description
# CHANGE THIS ONCE CODEBOOKS UPLOADED
pma_datasets['dv.dsDescription'] = np.where(pma_datasets['dv.title'].str.contains("Service Delivery Point"), 
                                         '[{"dsDescriptionValue": "' + pma_datasets['dv.dsDescription'] + ' More information about this dataset can be found in the corresponding codebook, accessible at <a href=https://doi.org/10.34976/f0vf-qd73>https://doi.org/10.34976/f0vf-qd73</a>' + '"}]',
                                         np.where(pma_datasets['dv.title'].str.contains("Client Exit"), 
                                          '[{"dsDescriptionValue": "' + pma_datasets['dv.dsDescription'] + ' More information about this dataset can be found in the corresponding codebook, accessible at <a href=https://doi.org/10.34976/1hrp-p268>https://doi.org/10.34976/1hrp-p268</a>' + '"}]',
                                          np.where(pma_datasets['dv.title'].str.contains("Household and Female"),
                                            '[{"dsDescriptionValue": "' + pma_datasets['dv.dsDescription'] + ' More information about this dataset can be found in the corresponding codebook, accessible at <a href=https://doi.org/10.34976/cjvx-z226>https://doi.org/10.34976/cjvx-z226</a>' + '"}]',
                                            '[{"dsDescriptionValue": "' + pma_datasets['dv.dsDescription'] + '"}]')))

# Add link to codebook in related material 

pma_datasets['dv.relatedMaterial'] = ['["Codebook: <a href=https://doi.org/10.34976/f0vf-qd73>https://doi.org/10.34976/f0vf-qd73</a>"]' if 'Service Delivery Point' in x else '["Codebook: <a href=https://doi.org/10.34976/1hrp-p268>https://doi.org/10.34976/1hrp-p268</a>"]' if 'Client Exit' in x else '["Codebook: <a href=https://doi.org/10.34976/cjvx-z226>https://doi.org/10.34976/cjvx-z226</a>"]' if 'Household and Female' in x else '["None"]' for x in pma_datasets['dv.title']]

# set dv.license to CC BY-NC 4.0
pma_datasets['dv.license'] = "CC BY-NC-SA 4.0"

# set dv.subject to ["Medicine, Health and Life Sciences"]
pma_datasets['dv.subject'] = '["Medicine, Health and Life Sciences"]'

# set dv.keyword to Keywords, split column into list on newline, lowercase everything except country somehow, and insert values into a dictionary of the form [{"keywordValue": "KeywordTerm1"}]
pma_datasets['dv.keyword'] = pma_datasets['dv.keyword'].str.split(',')

to_lowercase = ["Family Planning",
                "Reproductive Health",
                "Contraception",
                "Client Exit Interview",
                "Survey Research",
                "Codebook",
                "Health Facility Data",
               "Service Delivery Point",
               "Household and Female",
               "Longitudinal data"]

lowercase_keywords_column = []

for keywords in pma_datasets['dv.keyword']:
    stripped_keywords = [keyword.strip() for keyword in keywords]
    lowercase_keywords = [keyword.lower() if keyword in to_lowercase else keyword for keyword in stripped_keywords]
    lowercase_keywords_column.append(lowercase_keywords)

pma_datasets['dv.keyword'] = lowercase_keywords_column

keyword_column = []
for index, row in pma_datasets.iterrows():
	keyword_dict_list = []
	for keyword in row['dv.keyword']:
		keyword_dict_list.append({'keywordValue': keyword})
	keyword_column.append(keyword_dict_list)

keyword_column = [json.dumps(x, ensure_ascii = False) for x in keyword_column]

pma_datasets['dv.keyword'] = keyword_column

# set dv.topicClassification to [{"topicClassValue": "Maternal and Newborn Health"}]
pma_datasets['dv.topicClassification'] = ['[{"topicClassValue": "Covid-19"}]' if 'Covid-19' in x else '[{"topicClassValue": "Family Planning and Reproductive Health"}]' for x in pma_datasets['dv.title']]

# set dv.language to ["English"]
pma_datasets['dv.language'] = ['["English", "French"]' if any(s in x for s in ('Niger Phase', 'Ivoire', 'Democratic Republic of Congo', 'Burkina')) else '["English"]' for x in pma_datasets['dv.title']]

# set dv.grantNumber to agency and grant number
pma_datasets['dv.grantNumber'] = '[{"grantNumberAgency": "' + pma_datasets['dv.funder'] + '", "grantNumberValue": "' + pma_datasets['dv.grantNum'].astype(str) +'"}]'

# set dv.kindOfData = ["survey"]
pma_datasets['dv.kindOfData'] = '["survey"]'

# set dv.productionPlace to Johns Hopkins University
pma_datasets['dv.productionPlace'] = 'Johns Hopkins University'

# set dv.datasetContact to [{"datasetContactName": "For questions about the data contact Linnea Zimmerman via linnea.zimmerman@jhu.edu.", "datasetContactAffiliation": "Gates Institute for Populate and Reproductive Health, Johns Hopkins University", "datasetContactEmail": "linnea.zimmerman@jhu.edu"}, {"datasetContactName": "For questions about access to the data contact Johns Hopkins University Data Services via dataservices@jhu.edu. ", "datasetContactAffiliation": "Johns Hopkins University Data Services ", "datasetContactEmail": "dataservices@jhu.edu"}]
# this will change for each dataverse 
pma_datasets['dv.datasetContact'] = '[{"datasetContactName": "For questions about the data contact Phil Anglewicz via panglew1@jhu.edu.", "datasetContactAffiliation": "William H. Gates Sr. Institute for Population and Reproductive Health, Johns Hopkins University", "datasetContactEmail": "panglew1@jhu.edu"}, {"datasetContactName": "For questions about access to the data contact Johns Hopkins University Data Services via dataservices@jhu.edu. ", "datasetContactAffiliation": "Johns Hopkins University Data Services ", "datasetContactEmail": "dataservices@jhu.edu"}]'

# set dv.distributor to [{"distributorName": "Johns Hopkins University Data Services", "distributorAbbreviation": "JHUDS", "distributorURL": "https://dataservices.library.jhu.edu"}]
pma_datasets['dv.distributor'] = '[{"distributorName": "Johns Hopkins University Data Services", "distributorAbbreviation": "JHUDS", "distributorURL": "https://dataservices.library.jhu.edu"}]'

# set dv.producer as Addis Ababa University School of Public Health but insert into the correct json schema 
pma_datasets['dv.producer'] = '[{"producerName": "' + pma_datasets['dv.producer'] + '"}]'

pma_datasets = pma_datasets[["org.dataset_id",
              "org.doi",
              "org.to_upload",
              "dv.license",
              "dv.title",
             "dv.author", 
             "dv.dsDescription",
              "dv.subject",
              "dv.keyword",
              "dv.topicClassification",
              "dv.language",
              "dv.grantNumber",
              "dv.kindOfData",
              "dv.relatedMaterial",
              "dv.datasetContact",
              "dv.distributor",
              "dv.producer"]]

pma_datasets.to_csv("pma_datasets_toupload.csv", index=False)

# map the file dataset names to the dataset ids in pma_datasets
pma_datafiles = pma_datafiles.merge(pma_datasets[['dv.title', 'org.dataset_id']], how = "left", on = "dv.title")

pma_datafiles['org.dataset_id'] = [x for x in pma_datafiles['org.dataset_id']]

# increment datafiles 
pma_datafiles['org.datafile_id'] = range(1, len(pma_datafiles['dv.title'])+1)

pma_datafiles = pma_datafiles[['org.datafile_id', 'org.dataset_id', 'org.filename', 'folder']]

pma_datafiles.to_csv("pma_files_toupload.csv", index=False)