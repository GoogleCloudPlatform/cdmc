### Data Ingestion Deployment Guide

This guide covers the data ingestion aspects of the CDMC reference architecture. It is part of a larger deployment guide that includes metadata capturing, cataloging, lifecycle management, and reporting.  

1. The reference architecture uses the [TPC-DI dataset](https://www.tpc.org/tpcdi/default5.asp), which is a data integration benchmark. The data files are available for convenience from the `tpcdi` subfolder in the current directory. Alternatively, you can download them for free from [TPC.org](https://tpc.org/). 

2. Create a bucket on Google Cloud Storage and copy the tpcdi dataset to it. 

3. Open `LineageManager.py` and replace the `DL_API` and `SA_KEY` variables on lines 10 and 11 with your values. 

4. Open each of the 6 `load_*.py` scripts (e.g. `load_crm.py`, etc.) and replace the variables on lines 5-12 with your values. 

5. Install the python package dependencies:

`pip install -r requirements.txt`

6. Run the load scripts:

```
python load_crm.py
python load_finwire.py
python load_hr.py
python load_oltp.py
python load_reference.py
python load_sales.py
```

