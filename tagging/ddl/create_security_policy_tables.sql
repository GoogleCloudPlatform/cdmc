# Control 9 tables
create or replace table security_policy.default_methods(
	sensitive_category string, 
	geographical_region string, 
	encrypt_method string, 
	platform_deid_method string);
	
insert into security_policy.default_methods(sensitive_category, geographical_region, encrypt_method, platform_deid_method)
	values('Sensitive_Personal_Identifiable_Information', 'us-central1', 'CMEK+HSM', 'Nullify');
	
insert into security_policy.default_methods(sensitive_category, geographical_region, encrypt_method, platform_deid_method)
	values('Personal_Identifiable_Information', 'us-central1', 'CMEK+HSM', 'Hash (SHA256)');
	
insert into security_policy.default_methods(sensitive_category, geographical_region, encrypt_method, platform_deid_method)
	values('Sensitive_Personal_Information', 'us-central1', 'CMEK+HSM', 'Default Masking Value');

insert into security_policy.default_methods(sensitive_category, geographical_region, encrypt_method, platform_deid_method)
	values('Personal_Information', 'us-central1', 'CMEK+HSM', 'Default Masking Value');
	
insert into security_policy.default_methods(sensitive_category, geographical_region, encrypt_method, platform_deid_method)
	values('Public_Information', 'us-central1', NULL, NULL);	


create or replace table security_policy.permitted_methods(
	sensitive_category string, 
	geographical_region string, 
	encrypt_methods array<string>, 
	platform_deid_methods array<string>);

insert into security_policy.permitted_methods(sensitive_category, geographical_region, encrypt_methods, platform_deid_methods)
	values('Sensitive_Personal_Identifiable_Information', 'us-central1', ['CMEK+HSM', 'EKM'], ['SHA256Hash', 'Nullify', 'Default Masking Value']);

insert into security_policy.permitted_methods(sensitive_category, geographical_region, encrypt_methods, platform_deid_methods)
	values('Personal_Identifiable_Information', 'us-central1', ['CMEK+HSM', 'EKM'], ['SHA256Hash', 'Nullify', 'Default Masking Value']);

insert into security_policy.permitted_methods(sensitive_category, geographical_region, encrypt_methods, platform_deid_methods)
	values('Sensitive_Personal_Information', 'us-central1', ['CMEK+HSM', 'EKM'], ['SHA256Hash', 'Nullify', 'Default Masking Value']);

insert into security_policy.permitted_methods(sensitive_category, geographical_region, encrypt_methods, platform_deid_methods)
	values('Personal_Information', 'us-central1', ['CMEK+HSM', 'EKM'], ['SHA256Hash', 'Nullify', 'Default Masking Value']);

insert into security_policy.permitted_methods(sensitive_category, geographical_region, encrypt_methods, platform_deid_methods)
	values('Public_Information', 'us-central1', NULL, NULL);
	
