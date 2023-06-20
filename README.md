# Google Cloud CDMC Reference Architecture
This repository contains the CDMC reference architecture for Google Cloud. 

## Prerequisites
### GCP Setup

#### Projects required
Create two projects, as follows:
* A project to store the data, and run the controls against. For example `cdmc-confdata`
* A project to act as your data governance one, for example`cdmc-gov`

#### Infrastructure creation
The CDMC architecture relies on a number of GCP component which need to be provisioned.
The `setup.sh` script creates the necessary components. 
Before running the `setup.sh` script, make sure you have created and customised your 
`environment-variables.sh` file, using `environment-variables.example` as a template.
```
cp environment-variables.example environment-variables.sh
```
If at anypoint you need to set the environment variables, run the following command:
```
source environment-variables.sh
```

Onve you have customised the `environment-variables.sh`, create the infrastructure 
using the `setup.sh` convenience script.
```
source setup.sh
```

#### Application default credentials

In order to run the scripts in the repositories, you will need to set up the 
application default credentials for any machine used to run the script.

```
gcloud auth application-default login
```

You will be asked to login and enter an authorization code. 

The command will place the credentials file in the following location:
* Linux, macOS: `$HOME/.config/gcloud/application_default_credentials.json`
* Windows: `%APPDATA%\gcloud\application_default_credentials.json`


### Virtual Environment
It is advisable to create a virtual environment to install the required dependencies in
the machine you are running any script from. 
```
# Install virtual environment and activate
python3 -m venv .venv
source .venv/bin/activate
```


## Deployment Guide

Each component of the reference architecture has its own deployment guide. To deploy the entire reference architecture, follow the steps in each of the guides. There are 7 guides in total listed below:

- [data ingestion](https://github.com/GoogleCloudPlatform/cdmc/blob/main/data-ingestion/README.md) 
- [data scanning](https://github.com/GoogleCloudPlatform/cdmc/blob/main/data-scanning/README.md)  
- data quality (Mose)
- [tagging](https://github.com/GoogleCloudPlatform/cdmc/blob/main/tagging/README.md) 
- [record manager](https://github.com/GoogleCloudPlatform/bigquery-record-manager/blob/main/README.md)  
- [report engine](https://github.com/GoogleCloudPlatform/cdmc/blob/main/report-engine/README.md) 
- dashboard (Mark)