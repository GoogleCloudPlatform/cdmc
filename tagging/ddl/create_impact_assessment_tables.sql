-- control 10 policy table for impact assessments
-- assume that there will be impact assessment document for every data asset
-- The subject does not refer to the user who is querying the data, it refers to the subject of the data 
-- (i.e. in a customer table, it would be the location of the customer)
-- The ia_link is tied to a data asset, so it does not belong in the IA policy table
create or replace table impact_assessment.ia_policy(
   sensitive_type STRING,
   data_location STRING,
   subject_location STRING,
   ia_type STRING);

/* us-central1 */	
insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Personal_Identifiable_Information', 'us-central1', 'eu', 'DPIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Personal_Identifiable_Information', 'us-central1', 'uk', 'DPIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Personal_Identifiable_Information', 'us-central1', 'us', 'PIA');
   
insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
    values('Personal_Identifiable_Information', 'us-central1', 'br', 'PIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
	values('Personal_Identifiable_Information', 'us-central1', 'ww', 'PIA');
	
insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Sensitive_Personal_Identifiable_Information', 'us-central1', 'eu', 'DPIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Sensitive_Personal_Identifiable_Information', 'us-central1', 'uk', 'DPIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Sensitive_Personal_Identifiable_Information', 'us-central1', 'us', 'PIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Sensitive_Personal_Identifiable_Information', 'us-central1', 'br', 'PIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
	values('Sensitive_Personal_Identifiable_Information', 'us-central1', 'ww', 'PIA');
	
/* europe-west1 */	
insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Personal_Identifiable_Information', 'europe-west1', 'eu', 'DPIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Personal_Identifiable_Information', 'europe-west1', 'uk', 'DPIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Personal_Identifiable_Information', 'europe-west1', 'us', 'PIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
    values('Personal_Identifiable_Information', 'europe-west1', 'br', 'PIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Sensitive_Personal_Identifiable_Information', 'europe-west1', 'eu', 'DPIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Sensitive_Personal_Identifiable_Information', 'europe-west1', 'uk', 'DPIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
   values('Sensitive_Personal_Identifiable_Information', 'europe-west1', 'us', 'PIA');

insert into impact_assessment.ia_policy(sensitive_type, data_location, subject_location, ia_type)
    values('Sensitive_Personal_Identifiable_Information', 'europe-west1', 'br', 'PIA');
	

-- control 10 asset to subject location mapping table
-- The subject does not refer to the user who is querying the data, it refers to the subject of the data 
-- (i.e. in a customer table, it would be the location of the customer)
create or replace table impact_assessment.asset_ia_details(
   asset_name STRING,
   subject_location STRING,
   ia_type STRING,
   ia_link STRING,
   ia_creation_date DATE,
   ia_last_modified_date DATE);


insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.hr.Employee', 'ww', 'PIA', 'gs://impact_assessments/hr/Employee/report-ww.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.hr.Employee', 'uk', 'DPIA', 'gs://impact_assessments/hr/Employee/report-uk.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.hr.Employee', 'us', 'PIA', 'gs://impact_assessments/hr/Employee/report-us.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.oltp.Customer', 'ww', 'PIA', 'gs://impact_assessments/oltp/Customer/report-ww.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.oltp.Customer', 'uk', 'DPIA', 'gs://impact_assessments/oltp/Customer/report-uk.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.oltp.Customer', 'us', 'PIA', 'gs://impact_assessments/oltp/Customer/report-us.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.crm.NewCust', 'ww', 'PIA', 'gs://impact_assessments/crm/NewCust/report-ww.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.crm.NewCust', 'uk', 'DPIA', 'gs://impact_assessments/crm/NewCust/report-uk.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.crm.NewCust', 'us', 'PIA', 'gs://impact_assessments/crm/NewCust/report-us.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.crm.UpdCust', 'ww', 'PIA', 'gs://impact_assessments/crm/UpdCust/report-ww.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.crm.UpdCust', 'uk', 'DPIA', 'gs://impact_assessments/crm/UpdCust/report-uk.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.crm.UpdCust', 'us', 'PIA', 'gs://impact_assessments/crm/UpdCust/report-us.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.finwire.FINWIRE2006Q4_SEC', 'ww', 'PIA', 'gs://impact_assessments/finwire/FINWIRE2006Q4_SEC/report-ww.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.finwire.FINWIRE2006Q4_SEC', 'us', 'DPIA', 'gs://impact_assessments/finwire/FINWIRE2006Q4_SEC/report-us.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.finwire.FINWIRE1995Q4_SEC', 'ww', 'PIA', 'gs://impact_assessments/finwire/FINWIRE1995Q4_SEC/report-ww.pdf', '2023-01-01', '2023-02-02');

insert into impact_assessment.asset_ia_details(asset_name, subject_location, ia_type, ia_link, ia_creation_date, ia_last_modified_date) 
	values('sdw-conf-b1927e-bcc1.finwire.FINWIRE1995Q4_SEC', 'us', 'PIA', 'gs://impact_assessments/finwire/FINWIRE1995Q4_SEC/report-us.pdf', '2023-01-01', '2023-02-02');
