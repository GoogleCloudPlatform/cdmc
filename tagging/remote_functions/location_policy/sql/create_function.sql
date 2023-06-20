CREATE OR REPLACE FUNCTION `PROJECT_ID_GOV.remote_functions`.get_location_policy(project STRING) RETURNS STRING 
REMOTE WITH CONNECTION `PROJECT_ID_GOV.REGION.remote-function-connection` 
OPTIONS 
(endpoint = 'https://REGION-PROJECT_ID_GOV.cloudfunctions.net/get_location_policy'
);