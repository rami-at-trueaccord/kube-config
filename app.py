import ntpath

import boto3
from configparser import ConfigParser
from helpers import ColorMe
from os import path
import yaml

PROJECT_ROOT = path.dirname(path.abspath(__file__))

config = ConfigParser()
config_path = path.join(PROJECT_ROOT, 'config/config.ini')
print(f"Path is {config_path}")
config.read(config_path)
PROFILE = config.get('default', 'PROFILE')
API_VERSION = config.get('default', 'API_VERSION')
OUTPUT_PATH = config.get('default', 'OUTPUT_PATH')


def current_config():
    """ Display message for the config to be used in the $KUBECONFIG """
    return (f"You are set to use:\r"
            f"AWS Profile='{ColorMe.get(PROFILE, 'BLUE')}'\n"
            f"API Version='{ColorMe.get(API_VERSION, 'BLUE')}'\n"
            f"Writing to '{ColorMe.get(OUTPUT_PATH, 'BLUE')}'\n"
            f"Continue? (y/n): ")


# Confirm config is correct
go_on = input(current_config())
if go_on.lower() != 'y':
    quit('Terminating')

# Create session with AWS
session = boto3.session.Session(profile_name=PROFILE)
client = session.client('eks')

# Get EKS clusters
response = client.list_clusters()

# Common Config
config = {
    'apiVersion': 'v1',
    'clusters': [],
    'contexts': [],
    'current-context': '',
    'kind': 'Config',
    'preferences': {},
    'users': []
}

count = 0
for cluster in response['clusters']:
    desc = client.describe_cluster(name=cluster)
    name = desc['cluster']['name']
    endpoint = desc['cluster']['endpoint']
    cluster_arn = desc['cluster']['arn']
    cert = desc['cluster']['certificateAuthority']['data']

    # Clusters Config
    config['clusters'].append({
        'cluster': {
            'certificate-authority-data': cert,
            'server': endpoint
        },
        'name': cluster_arn
    })

    # Contexts Config
    config['contexts'].append({
        'context': {
            'cluster': cluster_arn,
            'user': cluster_arn,
        },
        'name': cluster_arn
    })

    # Users Config
    config['users'].append({
        'name': cluster_arn,
        'user': {
            'exec': {
                'apiVersion': API_VERSION,
                'args': [
                    '--region', 'us-west-2', 'eks', 'get-token', '--cluster-name', name
                ],
                'command': 'aws',
                'env': [{'name': 'AWS_PROFILE', 'value': PROFILE}],
                'interactiveMode': 'IfAvailable',
                'provideClusterInfo': False
            }
        }
    })

    # Print completeness percent because why not?
    count += 1
    percent = round((count / len(response['clusters'])) * 100)
    if percent < 100:
        print(f"{percent}% complete", end='\r')
    else:
        print(f"{percent}% complete")

# Write file
with open(OUTPUT_PATH, 'w+') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

# Reminders
print(f"Remember to move '{OUTPUT_PATH}' to '~/.kube/config'")
