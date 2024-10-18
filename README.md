## Milestone 2 Template

```
The files are empty placeholders only. You may adjust this template as appropriate for your project.
Never commit large data files,trained models, personal API Keys/secrets to GitHub
```

#### Project Milestone 2 Organization

```
.
├── LICENSE
├── README.md
└── src
    ├── art
    │   ├── Dockerfile
    │   ├── attacks
    │   └── docker-shell.sh
    ├── data_download_resnet
    │   ├── Dockerfile
    │   ├── data_download_resnet.py
    │   ├── docker-shell.sh
    │   └── requirements.txt
    ├── data_download_yolo
    │   ├── Dockerfile
    │   ├── data_download_yolo.py
    │   ├── docker-shell.sh
    │   └── requirements.txt
    ├── data_versioning_resnet
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── docker-entrypoint.sh
    │   ├── docker-shell.sh
    │   ├── resnet_dataset
    │   └── resnet_dataset.dvc
    ├── data_versioning_yolo
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── docker-entrypoint.sh
    │   ├── docker-shell.sh
    │   ├── yolo_dataset
    │   └── yolo_dataset.dvc
    ├── docker-compose.yml
    ├── resnet
    │   ├── Dockerfile
    │   ├── data
    │   ├── docker-shell.sh
    │   ├── models
    │   ├── python_files
    |   |   ├── model.py
    │   |   └── train_resnet.py
    │   └── requirements.txt
    └── yolo
        ├── Dockerfile
        ├── data
        ├── docker-shell.sh
        ├── python_files
        │   ├── runs
        |   ├── test_yolo.py
        |   ├── train_yolo.py
        |   ├── validate_yolo.py
        |   └── yolov5m.pt
        └── requirements.txt
```

# AC215 - Milestone2 - Advesarial Testing of Image Classification Models

**Team Members**
Jacob Huckelberry, Eli Dabkowsi, Ed Tang

**Group Name**
Black Knights Group

**Project**
In this project, we aim to develop an AI-powered cheese application. The app will feature visual recognition technology to identify various types of cheese and include a chatbot for answering all kinds of cheese-related questions. Users can simply take a photo of the cheese, and the app will identify it, providing detailed information. Additionally, the chatbot will allow users to ask cheese-related questions. It will be powered by a RAG model and fine-tuned models, making it a specialist in cheese expertise.

In this project, we aim to develop a framework to investigate the effects of adversarial attacks on image classification models. The app will feature two image classification networks trained to make medical diagnoses and recognize street signs--both critical functionalities with large consequences in instances of failure. The user will then be able to use the Adversarial Robustness Toolbox to perform preset attacks against these models to demonstrate their efficacy. Additionally, there will be an option to create mitigations against attacks and evaluate the resulting effects.

### Milestone2 ###

In this milestone, we have the components for data management, including versioning, as well as the image classification models and the adversarial robustness toolbox. 

**Data**

We have gathered two datasets:

The first dataset is from Kaggle (1) and is a dataset of over 50000 images of more than 40 classes of German traffic signs. The task associated with this dataset is classifying the datasets, and the preliminary model that we will finetune is Yolo. Along with the image data, there is also the shape of the sign as well as the color as features, although these may be ignored in the training process for a pure image classification task. 

The second dataset is from Hugging Face (2), and it is a collection of 10015 images of skin that are associated with seven different diagnoses. There are also metadata including the sex and age of the patient. The classification task is identifying the type of disease given the picture, and a resnet model will be trained on this dataset likely without the features. 

We have stored both datasets into Google Cloud Buckets.

**Data Pipeline Containers**

The Data Pipeline Containers for both the Resnet and Yolo models are identical:

1. One container downloads the data for the associated model from the cloud bucket locally. 

	**Input:** Source GCS location, data bucket location, local filesystem save location (provided via Docker).

	**Output:** Dataset stored in the local filesystem save location

2. Another container tracks the versioning of datasets with DVC (see data_versioning.md)

3. The model containers train on the datasets after loading and preprocessing steps

## Data Pipeline Overview


1. **`src/data_download_resnet/data_download_resnet.py`**
   This script downloads from the bucket containing the dataset locally.

2. **`src/data_download_resnet/Dockerfile`**
   The Dockerfile follows standard convention with modifications to work with Google Cloud Storage, including the necessary packages and credentials.

3. **`src/data_download_resnet/Pipfile`**
   The packages we used include google-cloud-storage for GCS interaction, pandas for data managment, and dvc/dvc-gs for version control.

4. **`src/data_versioning_resnet/Dockerfile`**
   Dockerfile that allows the container and associated files to create dvc files that track dataset versions through GCS remote storage.

5. **`src/data_versioning_resnet/docker-entrypoint.sh`**
   Run by the Dockerfile and accesses the GCS bucket data to mount it for model access.

6. The Yolo data pipeline files match those of resnet with different GCS buckets, dataset, and model architecture.

7. **`src/data_versioning_resnet/docker-shell.sh`**
   Builds and runs container -- universal function among all containers

## Models Overview

1. **`src/resnet/python_files/train_resnet.py`**
   This script handles data preprocessing and training for the resnet. The dataset is read, split into features (images) and response (diagnosis), split into training and validation splits, and then preprocessed by categorically encoding the diagnoses response variable. 

   The images are resized to (224x224). Then the data is then inputted into an ImageDataGenerator which increases the dataset size with transformations, the resulting training and validation sets are then ready for model training and evaulation.

   The script then compiles the resnet with the adam optimizer and categorical crossentropy loss with accuracy as the validation metric used for early stopping. Finally, the model is trained on the dataset and saved at the end of training to a `models` directory.

2. **`src/resnet/Dockerfile`**
   Follows standard conventions with modifications made to support model training.

3. **`src/resnet/requirements.txt`**
   We used the following packages for resnet model training and data preprocessing:
   - numpy
   - scipy
   - matplotlib
   - scikit-learn
   - pandas
   - yolov5
   - torch 
   - torchvision 
   - torchaudio
   - huggingface_hub==0.24.7
   - requests
   - ultralytics
   - ipython

4. **`src/resnet/model.py`**
   Defines the resnet model architecture with tensorflow to be called in `train_resnet.py`.

5. **`src/yolo/requirements.txt`**
   We used the following packages for yolo model training and data preprocessing:
   - numpy
   - scipy
   - matplotlib
   - scikit-learn
   - pandas
   - yolov5
   - torch 
   - torchvision 
   - torchaudio
   - huggingface_hub==0.24.7
   - requests
   - ultralytics
   - ipython

6. **`/src/yolo/Dockerfile`**
   Follows standard conventions with modifications made to support model training, being nearly identical to the resnet Dockerfile, adding libgli1 and libglib packages to be installed.

7. Yolo Files: To be Implemented for resnet
   - **`src/yolo/test_yolo.py`** and **`src/yolo/validate_yolo.py`** 
      - Generates **`src/yolo/test_yolo.py`**predictions and tests metrics on validation and test Yolo models.
   - **`src/yolo/train_yolo.py`**
      - Loads image files from street sign dataset, splits into training and validation splits, associates images with classification classes and stores data into yaml file.
      - Trains imported Yolo model on data stored in yaml file.

## Data Versioning Strategy:

### Explanation for Choice:

The team chose to use data version control (DVC) as our data versioning strategy, because it allows us to pull the data from our buckets and keep track of different versions of the dataset if we were to modify it in some way. Since the goal of our project is not necessarily to retrain the yolo and resnet models, rather to test adversarial attacks, we do not foresee there to be many different dataset versions. However, being able to use the cloud storage and ensure that teammates are pulling and working with the same datasets is crucial for development.

### Implementation:

There are two main datasets, traffic signs and cancer, that are used to train yolo and resnet. These are each set up with a `.dvc` file that stores the dataset metadata without the data itself. The data can then be downloaded from the buckets using our data download containers. If we are to make any modifications to the datasets, we will just update the `.dvc` files with the data versioning containers, ensuring that the most recent dataset is being used when it is pulled to be used for training.

Our current versioning containers are able to mount the google cloud storage bucket, and we are then able to make any modifications necessary.

#### Resnet `.dvc`:

```py
[core]
    remote = resnet_dataset
['remote "resnet_dataset"']
    url = gs://cancer-data-bucket/dvc_store
```

#### Yolo `.dvc`:

```py
[core]
    remote = yolo_dataset
['remote "yolo_dataset"']
    url = gs://traffic-sign-dataset/dvc_store
```
## Running Dockerfiles

Containers are run universally with `docker-shell.sh` scripts. Docker compose configuation files to be added later.


## Notebooks/Reports

**`deliverables/`**
   Contains screenshots for running containers and application mockup.


## Model Weights Link

You can find the weights we use for our ResNet and Yolo models here:

https://drive.google.com/drive/folders/12xqjhiSnE9g7RWqrwCIj-7xWYUFt366e?usp=drive_link


## Sources:

1. https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign
2. https://huggingface.co/datasets/marmal88/skin_cancer 