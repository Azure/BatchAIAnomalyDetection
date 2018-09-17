from azure.common.credentials import  ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
import azure.mgmt.batchai as batchai
import azure.mgmt.batchai.models as baimodels
import os
import json
import sys
import datetime
import time

config_file = sys.argv[1]
with open(config_file) as f:
    j = json.loads(f.read())

# Azure service principle login credentials
sp_tenant_id = j['TENANT_ID']
sp_client = j['CLIENT']
sp_key = j['KEY']

# Batch AI cluster info
resource_group_name = j['resource_group_name']
subscription_id = str(j['subscription_id'])
work_space = j['work_space']
cluster_name = j['cluster_name']
location = j['location']
command_line = j['command_line']
std_out_err_path_prefix = j['std_out_err_path_prefix']
config_file_path = j['config_file_path']
node_count = j['node_count']

# ACR info
acr_server = j['acr_server']
acr_image = j['acr_image']
acr_user = j['acr_user']
acr_password = j['acr_password']

# experiment
experiment_name = j['experiment_name'] + '_' + datetime.datetime.now().strftime('%y%m%d%H%M%S')

# job parameters
device_ids = j['device_ids']
tags = j['tags']
job_name_template = j['job_name']

credentials = ServicePrincipalCredentials(
    client_id=sp_client,
    secret=sp_key,
    tenant=sp_tenant_id
)

batchai_client = batchai.BatchAIManagementClient(credentials=credentials, subscription_id=subscription_id)
cluster = batchai_client.clusters.get(resource_group_name, work_space, cluster_name)
experiment = batchai_client.experiments.create(resource_group_name, work_space, experiment_name).result()

# run an async job for each sensor
for device_id in device_ids:
    for tag in tags:
        job_name = job_name_template.format(device_id, tag)
        custom_settings = baimodels.CustomToolkitSettings(command_line=command_line.format(device_id, tag, config_file_path))
        img_src_reg = baimodels.ImageSourceRegistry(
            server_url=acr_server,
            image=acr_image,
            credentials=baimodels.PrivateRegistryCredentials(username=acr_user,password=acr_password))
        container_settings = baimodels.ContainerSettings(image_source_registry=img_src_reg)
             
        print('command line: ' + custom_settings.command_line)
        params = baimodels.JobCreateParameters(cluster=baimodels.ResourceId(id=cluster.id),
                                               node_count=node_count,
                                               std_out_err_path_prefix=std_out_err_path_prefix,
                                               custom_toolkit_settings=custom_settings,
                                               container_settings=container_settings)

        batchai_client.jobs.create(resource_group_name, work_space, experiment.name, job_name, params)

     