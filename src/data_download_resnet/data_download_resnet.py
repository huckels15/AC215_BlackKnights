from google.cloud import storage
import os

# Set the environment variable for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/secrets.json'

def download_directory_from_gcs(bucket_name, source_directory, destination_directory):
    """
    Downloads all files from a GCS directory to a local directory.

    Args:
        bucket_name (str): The name of the GCS bucket.
        source_directory (str): The path to the directory in the GCS bucket (the "prefix").
        destination_directory (str): The local directory where the files should be saved.
    """
    # Create a Google Cloud Storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Ensure the destination directory exists
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # List all blobs in the GCS directory (with a given prefix)
    blobs = bucket.list_blobs(prefix=source_directory)

    # Download each file in the directory
    for blob in blobs:
        # Skip "directories" (GCS doesn't have real directories, just common prefixes)
        if blob.name.endswith("/"):
            continue

        # Create local path for the downloaded file
        file_name = os.path.basename(blob.name)  # Get the file name
        destination_file_name = os.path.join(destination_directory, file_name)

        # Download the blob to the local file path
        blob.download_to_filename(destination_file_name)

        print(f"Downloaded {blob.name} to {destination_file_name}")


if __name__ == '__main__':
    bucket_name = 'cancer-data-bucket' 
    source_directory = 'dvc_store/csvs/' 
    destination_directory = './data/' 

    download_directory_from_gcs(bucket_name, source_directory, destination_directory)




