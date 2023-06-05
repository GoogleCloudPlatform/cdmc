### Prerequisites
Make sure you have completed the steps in the [main README.md](../README.md) first,
and in particular you have configured the `environment-variables.sh` and 
created the requried infrastructure. 

### Data Ingestion 

The data ingestion aspects of the solution include copying the sample data to a 
Google Cloud Storage bucket and loading each dataset into BigQuery. 
The load scripts also record the data lineage of each table using Data Catalog's lineage API. 
Follow the steps below to deploy the data ingestions aspects of the solution.    

1. We use the [TPC-DI benchmark](https://www.tpc.org/tpcdi/default5.asp) as our sample data. 
You can download the dataset for free from [TPC.org](https://tpc.org/). Note that the download requires registration. 
Once you download the files, place them in the `data-ingestion/tpcdi-data` folder.
Your folder should look like this.
    ```
    $ tree tpcdi-data/
    tpcdi-data/
    ├── crm-data.zip
    ├── finwire-data.zip
    ├── hr-data.zip
    ├── oltp-data.zip
    ├── reference-data.zip
    └── sales-data.zip

    ```
1. Run the `load_data.sh` script.
 The script will:
    * Install the required dependencies
    * Load the data to GCS
    * Load the data from GCS to BQ

1. Once the script has completed, check whether the data is present in [BigQuery](https://pantheon.corp.google.com/bigquery)

### How to customise
Note how the data load process creates a lineage event for every file being loaded.
You can inspect the file `LineageManager.py` for an example on how to achieve this.
Creating a lineage event for every data load is critical for compliance with the data lineage controls.
Also, note how all the metadata automatically appears in Dataplex Datacatalog once the data is loaded in BigQuery.