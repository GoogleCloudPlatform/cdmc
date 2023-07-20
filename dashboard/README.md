# Instructions

This folder includes the configuration steps to enable the sample Looker Studio dashboard used in our CDMC Reference Architecture. The sample dashboard provides reports for a number of the CDMC key controls, combining data stored in BigQuery from the report engine findings and tag exports from Tag Engine. 

The installation steps below assume that the other CDMC Reference Architecture setup activities have already been performed and the environment is working correctly. However, for demonstration purposes, we also include an optional first step which creates BigQuery tables with demo finding and tag data. 

Note: The dashboard itself is aligned to data grouping in the sample TPC-DI data used throughout the Reference Architecture (e.g. crm, finwire, hr, oltp and sales datasets) and will require further customisation for your own data. 

## (Optional) Load dashboard demo data
If you want to explore the dashboards but do not yet have a fully working CDMC RA environment with Tag Engine and report engine, complete the following steps:

1. Ensure you are working in the desired project. 
```
gcloud config set project <your_cdmc_data_gov_project>
```

2. Create a new Google Cloud Storage bucket for your demo data
```
gcloud storage buckets create gs://<your_cdmc_demo_data_bucket>
```

3. Copy the four demo data Avro files in this repo into a Google Cloud Storage bucket
```
gsutil cp demo_data/*.avro gs://<your_cdmc_demo_data_bucket>/
```

4. Open `load_demo_data.sql` and find/replace the values for `<your_cdmc_data_gov_project>`, `<your_cdmc_demo_data_bucket>` and `<your_gcp_region>` as instructed

5. Save your changes

6. Run the amended script to create the BigQuery tables and load data from the Avro files
```
cat load_demo_data.sql | bq query --use_legacy_sql=false
```

In your project you should now see two new datasets, `cdmc_report` and `tag_exports` both with two tables inside. These tables should contain demo data for a demo project called '`sdw-conf-sample-project`.


## Create views against CDMC findings and tag export tables in BigQuery
The CDMC dashboard is reliant on a number of BigQuery views. Perform the following step to add the views to either your working CDMC Reference Architecture environment or the demo datasets created in the previous optional step. 

1. Ensure you are working in the desired project. 
```
gcloud config set project <your_cdmc_data_gov_project>
```

2. Open `create_views.sql` and find/replace the values for `<your_cdmc_data_gov_project>` and `<your_gcp_region>` as instructed

3. Save your changes

4. Run the modified script to create the BigQuery views
```
cat create_views.sql | bq query --use_legacy_sql=false
```

Depending on your permissions in the target environment, you may see an error about creating a view against INFORMATION_SCHEMA.JOBS_BY_FOLDER. This only affects the Purpose Tracking report in the dashboard, and the other reports will still work if this fails. 

## Create your own copy of the Looker Studio dashboard 
We have published our dashboard externally which allows other users to duplicate it in their own accounts. Once copied, the links will need to be updated to use your own data sources.

1. Request access to the Looker Studio sample CDMC dashboard by emailing cdmc-dashboard-access@google.com with details of the Google Cloud identity which you will use to access. A link to the dashboard will be shared with you. 

2. Once access has been granted, click on the dashboard link and from the drop down menu on the top right hand side of Looker Studio, select `Make a copy`

3. Ignore the warnings about the data sources and press `Copy report` 

4. Rename the report from `Copy of CDMC Dashboard` if desired to `<My organisation> CDMC Dashboard` 

## Link the new dashboard to your own BigQuery datasets
The dashboard should open in Looker Studio Edit mode. The dashboard's data sources now need to be linked to your own datasets. 

1. From the Looker Studio Resources menu select `Manage added data sources`

2. Starting at the top of the list, select the `Edit` action against the first datasource. Select your project from the `My Projects` list and the corresponding dataset and table which matches the previous data source name. 

3. Press the `Reconnect` button and apply the connection changes. Press `Done`

4. Repeat steps 2 and 3 for the other data sources. (If the INFORMATION_SCHEMA view creation failed in the earlier step, you will not be able to do this for the `information_schema_view` data source used by the Purpose Tracking report)

5. Press `Close` in the top right panel of the data sources view

6. Press `View` to see your new dashboard.

Congratulations! You should now have a fully working CDMC sample dashboard. 
