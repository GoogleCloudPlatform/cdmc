create or replace table entitlement_management.provider_agreement(provider_agreement_id string, sharing_scope_legal_entity string, sharing_scope_geography string, 
		data_asset_id string);

-- google legal entity reference: https://cloud.google.com/terms/google-entity
-- iso country code reference: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
		
insert into entitlement_management.provider_agreement(provider_agreement_id, sharing_scope_legal_entity, sharing_scope_geography, data_asset_id) 
	values('100', 'Google Cloud EMEA Limited', 'EU', 'finwire');

insert into entitlement_management.provider_agreement(provider_agreement_id, sharing_scope_legal_entity, sharing_scope_geography, data_asset_id) 
	values('200', 'Google', 'US', 'finwire');
	
insert into entitlement_management.provider_agreement(provider_agreement_id, sharing_scope_legal_entity, sharing_scope_geography, data_asset_id) 
	values('300', 'Google Cloud EMEA Limited', 'UK', 'crm');

insert into entitlement_management.provider_agreement(provider_agreement_id, sharing_scope_legal_entity, sharing_scope_geography, data_asset_id) 
	values('400', 'Google LLC', 'US', 'crm');

insert into entitlement_management.provider_agreement(provider_agreement_id, sharing_scope_legal_entity, sharing_scope_geography, data_asset_id) 
	values('500', 'Google Cloud EMEA Limited', 'EU', 'crm');

insert into entitlement_management.provider_agreement(provider_agreement_id, sharing_scope_legal_entity, sharing_scope_geography, data_asset_id) 
	values('600', 'Google Cloud Japan G.K.', 'Japan', 'oltp');

insert into entitlement_management.provider_agreement(provider_agreement_id, sharing_scope_legal_entity, sharing_scope_geography, data_asset_id) 
	values('700', 'Google LLC', 'US', 'hr');

insert into entitlement_management.provider_agreement(provider_agreement_id, sharing_scope_legal_entity, sharing_scope_geography, data_asset_id) 
	values('701', 'Google Cloud EMEA Limited', 'UK', 'hr');

insert into entitlement_management.provider_agreement(provider_agreement_id, sharing_scope_legal_entity, sharing_scope_geography, data_asset_id) 
	values('800', 'PT Google Cloud Indonesia', 'ID', 'sales');

insert into entitlement_management.provider_agreement(provider_agreement_id, sharing_scope_legal_entity, sharing_scope_geography, data_asset_id) 
	values('801', 'Google New Zealand Limited', 'NZ', 'sales');


create or replace table entitlement_management.use_purpose(use_id string, use_description string, operation string,  data_asset_id string);

insert into entitlement_management.use_purpose(use_id, use_description, operation, data_asset_id)
	values ('1', 'Direct marketing', 'SELECT', 'finwire');

insert into entitlement_management.use_purpose(use_id, use_description, operation, data_asset_id)
	values ('2', 'Analytics', 'INSERT',	'crm');

insert into entitlement_management.use_purpose(use_id, use_description, operation, data_asset_id)
	values ('2', 'Analytics', 'SELECT',	'crm');

insert into entitlement_management.use_purpose(use_id, use_description, operation, data_asset_id)
	values ('3', 'Customer service', 'SELECT',	'crm');

insert into entitlement_management.use_purpose(use_id, use_description, operation,  data_asset_id)
	values ('4', 'User research', 'SELECT',	'oltp');

insert into entitlement_management.use_purpose(use_id, use_description, operation,  data_asset_id)
	values ('5', 'Analytics', 'SELECT', 'finwire');
	
insert into entitlement_management.use_purpose(use_id, use_description, operation,  data_asset_id)
	values ('6', 'Analytics', 'SELECT', 'hr');
	
insert into entitlement_management.use_purpose(use_id, use_description, operation,  data_asset_id)
	values ('61', 'RTO Research', 'SELECT', 'hr');

insert into entitlement_management.use_purpose(use_id, use_description, operation,  data_asset_id)
	values ('8', 'Anomaly Detection', 'SELECT', 'sales');

insert into entitlement_management.use_purpose(use_id, use_description, operation,  data_asset_id)
	values ('81', 'Analytics', 'SELECT', 'sales');


create or replace table entitlement_management.data_asset(data_asset_id string, data_asset_name string, data_owner_name string, data_owner_email string, is_authoritative bool);
	
insert into entitlement_management.data_asset(data_asset_id, data_asset_name, data_owner_name, data_owner_email, is_authoritative) 
	values('finwire', 'sdw-conf-b1927e-bcc1.finwire.FINWIRE*', 'Eduardo Marreto', 'edumarreto@secure-blueprint-demo-one.ongcp.co', True);
	
insert into entitlement_management.data_asset(data_asset_id, data_asset_name, data_owner_name, data_owner_email, is_authoritative) 
	values('crm', 'sdw-conf-b1927e-bcc1.crm.*', 'Svitlana Gavrylova', 'gavrylova@secure-blueprint-demo-one.ongcp.co', True);
	
insert into entitlement_management.data_asset(data_asset_id, data_asset_name, data_owner_name, data_owner_email, is_authoritative) 
	values('oltp', 'sdw-conf-b1927e-bcc1.oltp.*', 'Julien Phalip', 'jphalip@secure-blueprint-demo-one.ongcp.co', False);
	
insert into entitlement_management.data_asset(data_asset_id, data_asset_name, data_owner_name, data_owner_email, is_authoritative) 
	values('hr', 'sdw-conf-b1927e-bcc1.hr.*', 'Mark Tomlinson', 'marktomlinson@secure-blueprint-demo-one.ongcp.co', False);	

insert into entitlement_management.data_asset(data_asset_id, data_asset_name, data_owner_name, data_owner_email, is_authoritative) 
	values('sales', 'sdw-conf-b1927e-bcc1.sales.*', 'Mose Tronci', 'mtronci@secure-blueprint-demo-one.ongcp.co', True);	
	

/* This table references the provider_agreement_id and use_id fields */
create or replace table entitlement_management.consumer_agreement(user_email string, user_legal_entity string, sharing_scope_legal_entity string, sharing_scope_geography string, provider_agreement_id string, use_id string, approval_date date, valid_until_date date, ia_review_date date);

insert into entitlement_management.consumer_agreement(user_email, user_legal_entity, sharing_scope_legal_entity, sharing_scope_geography, provider_agreement_id, use_id, approval_date, valid_until_date, ia_review_date) 
  values('mtronci@secure-blueprint-demo-one.ongcp.co', 'Google Cloud EMEA Limited', 'Google', 'UK', '100', '2', '2022-07-01', '2023-06-30', '2023-01-01');
			
insert into entitlement_management.consumer_agreement(user_email, user_legal_entity, sharing_scope_legal_entity, sharing_scope_geography, provider_agreement_id, use_id, approval_date, valid_until_date, ia_review_date) 
  values('scohen@secure-blueprint-demo-one.ongcp.co', 'Google LLC', 'Google', 'US', '400', '2', '2022-08-01', '2023-07-31', '2023-01-01');

insert into entitlement_management.consumer_agreement(user_email, user_legal_entity, sharing_scope_legal_entity, sharing_scope_geography, provider_agreement_id, use_id, approval_date, valid_until_date, ia_review_date) 
  values('mtronci@secure-blueprint-demo-one.ongcp.co', 'Google Cloud EMEA Limited', 'Google Cloud EMEA Limited', 'EU', '500', '3', '2022-08-15', '2023-09-14', '2023-01-01');

insert into entitlement_management.consumer_agreement(user_email, user_legal_entity, sharing_scope_legal_entity, sharing_scope_geography, provider_agreement_id, use_id, approval_date, valid_until_date, ia_review_date) 
  values('jphalip@secure-blueprint-demo-one.ongcp.co', 'Google LLC', 'Google LLC', 'US', '200', '1', '2022-08-18', '2023-08-19', '2023-01-01');
