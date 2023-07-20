### Data Scanning

The data scanning aspects of the solution consists of using Data Loss Prevention (DLP) to create inspection jobs that scan each table in the sample dataset. The jobs produce a findings table with all the infotypes associated with each sensitive field. Follow the steps below to deployment the data scanning aspects of the solution. 

This guide assumes that you have already completed the data ingestion deployment.   

1. Install the python package dependencies:
    ```
    pip install -r requirements.txt
    ```

1. Run the inspection script, passing the the number of days to scan for data loss (0 runs the inspection now):
    ```
    python3 inspect_datasets_schedule.py --scan_period_days 0
    ```

