# Data Versioning Strategy:

## Explanation for Choice:

The team chose to use data version control (DVC) as our data versioning strategy, because it allows us to pull the data from our buckets and keep track of different versions of the dataset if we were to modify it in some way. Since the goal of our project is not necessarily to retrain the yolo and resnet models, rather to test adversarial attacks, we do not foresee there to be many different dataset versions. However, being able to use the cloud storage and ensure that teammates are pulling and working with the same datasets is crucial for development.

## Implementation:

There are two main datasets, traffic signs and cancer, that are used to train yolo and resnet. These are each set up with a `.dvc` file that stores the dataset metadata without the data itself. The data can then be downloaded from the buckets using our data download containers. If we are to make any modifications to the datasets, we will just update the `.dvc` files with the data versioning containers, ensuring that the most recent dataset is being used when it is pulled to be used for training.

Our current versioning containers are able to mount the google cloud storage bucket, and we are then able to make any modifications necessary.

### Resnet `.dvc`:

```py
[core]
    remote = resnet_dataset
['remote "resnet_dataset"']
    url = gs://cancer-data-bucket/dvc_store
```

### Yolo `.dvc`:

```py
[core]
    remote = yolo_dataset
['remote "yolo_dataset"']
    url = gs://traffic-sign-dataset/dvc_store
```