# Scoring Anomaly Detection Models at Scale using Batch AI
In this repository you will find a set of scripts and commands that help you build a scalable solution for scoring many models in parallel using Batch AI.

The solution can be used as a template and can generalize to different problems. The problem addressed here is monitoring the operation of a large number of devices in an IoT setting, where each device sends sensor readings continuously. We assume there are pre-trained [anomaly detection models](http://scikit-learn.org/stable/modules/outlier_detection.html#outlier-detection) (one for each device) that need to be used to predict whether a series of measurements, that are aggregated over a predefined time interval, correspond to an anomaly or not.

## Architecture
![System Architecture](./architecture.PNG)

This solution consists of several Azure cloud services that allow upscaling and downscaling resources according to need. The services and their role in this solution are described below.

### Blob Storage
Blob containers are used to store the pre-trained models, the data, and the output predictions. The models that we upload to blob storage in the [*create_resources.ipynb*](create_resources.ipynb) notebook are [One-class SVM](http://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html) models that are trained on data that represents values of different sensors of different devices. We assume that the data values are aggregated over a fixed interval of time. In real-world scenarios, this could be a stream of sensor readings that need to be filtered and aggregated before being used in training or real-time scoring. For simplicity, we use the same data file when executing scoring jobs.

### Batch AI
Batch AI is the distributed computing engine used here. It allows spinning up virtual machines on demand with an auto-scaling option, where each node in the Batch AI cluster runs a scoring job for a specific sensor. The scoring Python [script](batchai/predict.py) is run in Docker containers that are created on each node of the cluster.

### Logic Apps
Logic Apps provide an easy way to create the runtime workflow and scheduling for the solution. In our case, we create a Logic App that runs hourly Batch AI jobs. The jobs are submitted using a Python [script](sched/submit_jobs.py) that also runs in a Docker container.

### Container Registry
The Docker images used in both Batch AI and Logic Apps are created in the [*create_resources.ipynb*](create_resources.ipynb) notebook and pushed to an Azure Container Registry (ACR). ACR provides a convenient way to host images and instantiate containers through other Azure services.


> For more information on these services, check the documentation links provided below in the *Links* section. 

## Prerequisites
- Python >=3.5
- [Jupyter Notebook](http://jupyter.org/index.html) - *pip install jupyter*
- [azure package 4.0.0](https://pypi.org/project/azure/) - *pip install azure==4.0.0*
- [Azure CLI 2.0](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Docker](https://www.docker.com/)
- [jq](https://stedolan.github.io/jq/) - *sudo apt-get install jq*


> *All scripts and commands were tested on an Ubuntu 16.04 LTS system.*

Once all prerequisites are installed, clone or download this repo and start creating the required resources.

## Creating Azure Resources
The following notebook contains all Azure CLI and Docker commands needed to create resources in your Azure subscription, as well as configurations of Batch AI and scoring Python scripts. 

[create_resources.ipynb](create_resources.ipynb)

## Validating Deployments and Jobs Execution 
After all resources are created, you can check your resource group in the portal and validate that all components have been deployed successfully. 

> In addition, you would need to navigate to the ACI API connection in the portal and authenticate by either using your service principle info or sign in using your email and password/pin.

Under *Batch AI Cluster > Jobs*, you should see the experiment and scoring jobs, as soon as the Logic App is triggered.

Under *Storage Account > Blobs*, you should see the predictions CSV files in the *predictions* container, after the Batch AI jobs finish successfully.


## Cleanup
If you wish to delete all created resources, run the following CLI command to delete the resource group and all underlying resources.

```sh
az group delete --name <resource group name>
```

## Links
- [End-to-End Anomaly Detection Jobs using Azure Batch AI](https://github.com/saidbleik/batchai_mm_ad)
- [Batch AI Documentation](https://docs.microsoft.com/en-us/azure/batch-ai/)
- [Logic Apps Documentation](https://docs.microsoft.com/en-us/azure/logic-apps/)
- [Azure Blob Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction)

## Contributing
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
