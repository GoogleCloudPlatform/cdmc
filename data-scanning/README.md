### Data Scanning

The data scanning aspects of the solution consists of using Data Loss Prevention (DLP) to create inspection jobs that scan each table in the sample dataset. The jobs produce a findings table with all the infotypes associated with each sensitive field. Follow the steps below to deployment the data scanning aspects of the solution. 

This guide assumes that you have already completed the data ingestion deployment.   

1. Enable the DLP API in the GCP project where your data assets reside. 

2. Open `inspect_datasets.py` and replace the variables on lines 18, 19, and 22 with your own values. 

3. Adjust the inspection job schedule defined by `scan_period_days` on line 29. The default value triggers the job once per day. 

4. Install the python package dependencies:

`pip install -r requirements.txt`

5. Run the inspection script:

`python inspect_datasets.py`

