CREATE OR REPLACE FUNCTION `PROJECT_ID_GOV.remote_functions`.get_bytes_transferred(mode STRING, 
											project STRING, dataset STRING, table STRING) RETURNS FLOAT64 
REMOTE WITH CONNECTION `PROJECT_ID_GOV.REGION.remote-function-connection` 
OPTIONS 
(endpoint = 'https://REGION-PROJECT_ID_GOV.cloudfunctions.net/get_bytes_transferred'
);