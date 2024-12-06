from yolov5 import train
import os
from sklearn.model_selection import train_test_split
from google.cloud import storage
import argparse
import yaml

def download_yolo_data(bucket_name, source_directory, destination_directory):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=source_directory)

    for blob in blobs:
        if blob.name.endswith("/"):
            continue

        relative_path = os.path.relpath(blob.name, source_directory)
        local_path = os.path.join(destination_directory, relative_path)
        local_dir = os.path.dirname(local_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        blob.download_to_filename(local_path)

        print(f"Downloaded {blob.name}")

def make_yaml():
    class_names = ['prohibitory', 'danger', 'mandatory', 'other']

    data_dir = os.path.abspath('yolo_data/ts/ts')
    train_image_list = os.path.abspath('yolo_data/train_images.txt')
    val_image_list = os.path.abspath('yolo_data/val_images.txt')
    yaml_file = os.path.abspath('yolo_data/dataset.yaml')

    image_files = [f for f in os.listdir(data_dir) if f.endswith('.jpg')]

    train_files, val_files = train_test_split(image_files, test_size=0.2, random_state=42)

    with open(train_image_list, 'w') as f:
        for item in train_files:
            f.write("%s\n" % os.path.join(data_dir, item))

    with open(val_image_list, 'w') as f:
        for item in val_files:
            f.write("%s\n" % os.path.join(data_dir, item))

    data = {
        'train': train_image_list,
        'val': val_image_list,
        'nc': len(class_names),
        'names': {i: name for i, name in enumerate(class_names)}
    }

    with open(yaml_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)


def upload_results_to_gcs(bucket_name, subdirectory, source_directory):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            local_path = os.path.join(root, file)
            gcs_path = os.path.join(subdirectory, os.path.relpath(local_path, source_directory))
            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(local_path)
            print(f"Uploaded {local_path} to {gcs_path} in bucket {bucket_name}")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--model_name", 
    dest="model_name", 
    default="yolo", 
    type=str, 
    help="Model name"
    )
parser.add_argument(
    "--epochs", 
    dest="epochs", 
    default=1, 
    type=int, 
    help="Number of epochs."
    )
parser.add_argument(
    "--batch_size", 
    dest="batch_size", 
    default=8, 
    type=int, 
    help="Size of a batch."
    )
parser.add_argument(
    "--model_bucket", 
    dest="model_bucket", 
    default="yolo-models-ac215", 
    type=str, 
    help="Bucket for models."
    )
parser.add_argument(
    "--data_bucket", 
    dest="data_bucket", 
    default="traffic-sign-dataset", 
    type=str, 
    help="Bucket for data."
    )

parser.add_argument(
    "--exp_num", 
    dest="exp_num", 
    default="", 
    type=str, 
    help="Number for storage"
    )

args = parser.parse_args()

if __name__ == "__main__":

    download_yolo_data(args.data_bucket, 'dvc_store/data/', './yolo_data/')
    make_yaml()

    train.run(
        img=416,
        batch=args.batch_size,
        epochs=args.epochs,
        data="yolo_data/dataset.yaml",
        weights='yolov5m.pt',
        device='0',
        workers=1
    )

output_directory = './runs/train/exp'
upload_results_to_gcs(args.model_bucket, args.exp_num , output_directory)
