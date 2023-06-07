# Instructions

This is folder incldues the configuration for some of the DQ rules of the TPC-DI dataset,
using a minimalistic configuration of `cloud-data-quality`.
For convenience, we include a deployment script which creates a Cloud Run job that can execute the 
data quality rules.

## Configuration
All of the configuration is in the `configs` folder. Note how common rules are in the `common.yml` file and there is a config file per entity of the TCP-DI dataset, containing fields and rules bindings.

You can customise the configuration to your requirements.

## Deployment
For convenience, we have provided a deployment script which performes the following:
* Builds a docker image with the cloud-dq binaries and the configuraiton, and uploads to GCR
* Creates a CloudRun job, passing the following parameters: 
    * project_id where the data resides
    * project_id of the data governance, where DQ runs 
    * region where DQ runs 
    * dataset used to store the DQ results

You can deploy by executing the following script:
```
. ./deploy_cdmc-dq.sh
```

## Execute on cloud run
Once you have deployed on CloudRun, simply use the following command to execute:
```
gcloud config set project $PROJECT_ID_GOV
gcloud run jobs execute cloud-dq --region $REGION
```

## [OPTIONAL] Execute locally
The Cloud-DQ binaries requires a specific OS version and Python version, so if you want to 
execute locally it is best to do that within a container.

To build the container locally:
```
docker build -t cloud-dq .
```

To execute the container locally: 
```
docker run -v $HOME/.config/gcloud:/root/.config/gcloud cloud-dq $PROJECT_ID $PROJECT_ID_GOV $REGION $CLOUDDQ_BIGQUERY_DATASET
```
Note how we map the folder with the ADC token to the container to provide access, and pass the 
parameters which are eventually propagated to the `run_dq_engine.sh`

## Production deployment
For production deployment, we recommend using [Dataplex data quality tasks](https://cloud.google.com/dataplex/docs/check-data-quality)
