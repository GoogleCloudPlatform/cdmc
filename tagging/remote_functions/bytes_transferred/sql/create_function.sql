CREATE OR REPLACE FUNCTION `cdmc-gov-388611.remote_functions`.get_bytes_transferred(mode STRING, 
											project STRING, dataset STRING, table STRING) RETURNS FLOAT64 
REMOTE WITH CONNECTION `cdmc-gov-388611.us-central1.remote-function-connection` 
OPTIONS 
(endpoint = 'https://us-central1-cdmc-gov-388611.cloudfunctions.net/get_bytes_transferred'
);