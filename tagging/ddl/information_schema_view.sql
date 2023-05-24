create or replace view entitlement_management.information_schema_view as 
select * from (
select * from (
SELECT
    cast(i.start_time as date) as job_date,
	i.user_email AS user_id,
    i.statement_type AS operation, 
    CONCAT(rf.project_id,'.',rf.dataset_id,'.',rf.table_id) as data_asset,
    l.key as key,
	l.value as value
FROM
    region-us-central1.INFORMATION_SCHEMA.JOBS_BY_PROJECT as i,
    unnest(i.referenced_tables) as rf,
	unnest(i.labels) as l
UNION ALL
SELECT
    cast(i.start_time as date) as job_date,
	i.user_email AS user_id,
    i.statement_type AS operation, 
    CONCAT(rf.project_id,'.',rf.dataset_id,'.',rf.table_id) as data_asset,
    NULL as key,
	NULL as value
FROM
    region-us-central1.INFORMATION_SCHEMA.JOBS_BY_PROJECT as i,
    unnest(i.referenced_tables) as rf
);
