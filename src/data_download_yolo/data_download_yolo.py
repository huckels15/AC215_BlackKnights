from google.cloud import storage
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/secrets.json'

def download_directory_from_gcs(bucket_name, source_directory, destination_directory):
    """
    The workflow here is relatively straight forward. We make a client and then obtain the 
    bucket that is specified within the function definition. We then proceed to obtain all of the 
    blobs, or files, within the bucket. If the blobs name ends with a /, we know that it is a directory,
    so in order to keep the same file structure we continue to sift through the blob, creating further
    directories within our local machine in accordance with the structure that is specified within the blob. 
    We then download the directory structure from within the bucket to the user specified destination 
    and download that to the local machine. 
    """
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


if __name__ == '__main__':
    bucket_name = 'traffic-sign-dataset' 
    source_directory = 'dvc_store/data/' 
    destination_directory = './yolo_data/' 

    download_directory_from_gcs(bucket_name, source_directory, destination_directory)
