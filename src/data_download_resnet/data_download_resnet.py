from google.cloud import storage
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/secrets.json'

def download_directory_from_gcs(bucket_name, source_directory, destination_directory):
    """
    The workflow here is relatively straight forward. We make a client and then obtain the 
    bucket that is specified within the function definition. We then proceed to obtain all of the 
    blobs, or files, within the bucket. If the blobs name ends with a /, we know that it is a directory,
    so in order to keep the same file structure we continue to sift through the blob until we reach
    the actual file that is specified by the basename function. We then join that name with the 
    userspecified destination and download that to the local machine. 
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=source_directory)
    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        
        file_name = os.path.basename(blob.name)
        destination_file_name = os.path.join(destination_directory, file_name)
        blob.download_to_filename(destination_file_name)

        print(f"Downloaded {blob.name}")


if __name__ == '__main__':
    bucket_name = 'cancer-data-bucket' 
    source_directory = 'dvc_store/csvs/' 
    destination_directory = './data/' 
    download_directory_from_gcs(bucket_name, source_directory, destination_directory)




