import create_template as template 
import argparse

project_id = 'sdw-data-gov-b1927e-dd69' # cdmc project
region = 'us-central1'

parser = argparse.ArgumentParser(description="runs create_template.py")
parser.add_argument('yaml_file', help='Path to your yaml file')
args = parser.parse_args()

#yaml_file = 'dg_template.yaml'

template.create_template(project_id, region, args.yaml_file)
