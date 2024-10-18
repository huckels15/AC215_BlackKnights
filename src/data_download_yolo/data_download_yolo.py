from google.cloud import storage
import os

# Set the environment variable for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/secrets.json'

def download_directory_from_gcs(bucket_name, source_directory, destination_directory):
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

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

        print(f"Downloaded {blob.name} to {local_path}")


if __name__ == '__main__':
    bucket_name = 'traffic-sign-dataset' 
    source_directory = 'dvc_store/data/' 
    destination_directory = './data/' 

    download_directory_from_gcs(bucket_name, source_directory, destination_directory)
