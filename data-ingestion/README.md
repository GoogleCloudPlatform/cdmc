### Data Ingestion 

The data ingestion aspects of the solution include copying the sample data to a Google Cloud Storage bucket and loading each dataset into BigQuery. The load scripts also record the data lineage of each table using Data Catalog's lineage API. Follow the steps below to deploy the data ingestions aspects of the solution.    

1. We use the [TPC-DI benchmark](https://www.tpc.org/tpcdi/default5.asp) as our sample data. This dataset is include in this repo for convenience, you will find it in the `tpcdi` subfolder. Alternatively, you can download the dataset for free from [TPC.org](https://tpc.org/). Note that the download requires registration. 

2. Create a bucket on Google Cloud Storage and copy the tpcdi dataset into it. 

3. Open `LineageManager.py` and replace the `DL_API` and `SA_KEY` variables on lines 24 and 25 with your values. 

4. Open each of the 6 `load_*.py` scripts (e.g. `load_crm.py`, etc.) and replace the variables on lines 19-26 with your values. 

5. Install the python package dependencies:

`pip install -r requirements.txt`

6. Run each of the load scripts below to create and populate the BigQuery datasets with all the data assets in the TPC-DI benchmark:

```
python load_crm.py
python load_finwire.py
python load_hr.py
python load_oltp.py
python load_reference.py
python load_sales.py
```

