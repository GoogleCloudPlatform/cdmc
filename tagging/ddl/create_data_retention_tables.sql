# control 11 tables
create or replace table data_retention.retention_policy(sensitive_category string, geographical_region string, retention_period_days int64, expiration_action string);

insert into data_retention.retention_policy values('Sensitive_Personal_Identifiable_Information', 'us-central1', 60, 'Purge');
insert into data_retention.retention_policy values('Personal_Identifiable_Information', 'us-central1', 90, 'Archive');
insert into data_retention.retention_policy values('Sensitive_Personal_Information', 'us-central1', 180, 'Archive');
insert into data_retention.retention_policy values('Personal_Information', 'us-central1', 180, 'Archive');

		
