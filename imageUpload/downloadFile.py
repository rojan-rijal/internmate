def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f'downloads/{file_name}'
    s3.Bucket(bucket).download_file(file_name, output)

    return output

