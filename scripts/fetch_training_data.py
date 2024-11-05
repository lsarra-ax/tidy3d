import concurrent
import os
import boto3
from boto3.dynamodb.conditions import Key
import csv
import tempfile
from botocore.exceptions import ClientError

from tidy3d import Simulation
from tidy3d.components.metadata import simulation_metadata

import threading

# This is the shared resource
index = 0

# Create a lock
lock = threading.Lock()
# Specify your AWS credentials
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")
region_name = os.getenv("AWS_REGION")
# Create a Boto3 DynamoDB resource with credentials
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=aws_access_key,
                          aws_secret_access_key=aws_secret_key,
                          region_name=region_name)
bucket_name = 'flow360studio'
s3 = boto3.client('s3'
                  , aws_access_key_id=aws_access_key
                  , aws_secret_access_key=aws_secret_key)

solver_task_table = dynamodb.Table("flow360-solver-task")
result = []

response = solver_task_table.query(
    IndexName="Status-SubmitTime-index",
    KeyConditionExpression=Key('Status').eq("success"),
    ScanIndexForward=False,  # Sorts the results in descending order
    Limit=10000  # Limits the number of items returned
)
result.extend(response['Items'])

def increment_index():
    global index
    with lock:  # Acquire the lock before modifying the shared resource
        index += 1
        print(f"The index is now {index}")

def download_simulation(user_id, task_id):
    gz_object_key = f'users/{user_id}/{task_id}/simulation.hdf5.gz'
    hdf5_object_key = f'users/{user_id}/{task_id}/simulation.hdf5'

    # Extract the file name from the object key
    gz_file_name = os.path.basename(gz_object_key)
    hdf5_file_name = os.path.basename(hdf5_object_key)

    # Function to check if an object exists in S3
    def does_s3_object_exist(bucket, key):
        try:
            s3.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise

    # Check if the .gz file exists
    if does_s3_object_exist(bucket_name, gz_object_key):
        with tempfile.NamedTemporaryFile(suffix=gz_file_name, delete=True) as tmp_file:
            print(f"Temporary file created at {tmp_file.name}")
            s3.download_file(bucket_name, gz_object_key, tmp_file.name)
            print(f"File downloaded successfully: {tmp_file.name}")
            sim = Simulation.from_file(tmp_file.name)
    elif  does_s3_object_exist(bucket_name, hdf5_object_key):
        # If the .gz file does not exist, download the .hdf5 file
        try:
            with tempfile.NamedTemporaryFile(suffix=hdf5_file_name, delete=True) as tmp_file:
                print(f"Temporary file created at {tmp_file.name}")
                s3.download_file(bucket_name, hdf5_file_name, tmp_file.name)
                print(f"File downloaded successfully: {tmp_file.name}")
                sim = Simulation.from_file(tmp_file.name)
            print('File simulation.hdf5 downloaded successfully')
        except ClientError as e:
            print(f"Error downloading file: {e}")

    return sim

def process(writer, item):
    increment_index()
    task_id = item['TaskId']
    user_id = item['UserId']
    node_size = item.get('NodeSize')
    storage_size = item.get('StorageSize')
    task_start_time = item.get('TaskStartTime') # before files download
    solver_start_time =  item.get('SolverStartTime')
    solver_end_time = item.get('SolverFinishTime')
    task_end_time = item.get('TaskFinishTime')  # after the on-prem simulation is done. regardless the file upload times
    num_of_gpu = item.get('NumProcessors')
    worker = item.get('Worker')
    gpu_type = None
    if 'a5k' in worker:
        gpu_type = 'a5000'
    elif 'node' in worker:
        gpu_type = '1080ti'
    elif 'cell' in worker:
        gpu_type = 'a100'
    elif 'h200' in worker:
        gpu_type = 'h200'

    solver_version = item.get('SolverVersion')
    real_flex_credit = item.get('RealFlexUnit')
    real_time_steps = item.get('TimeSteps')

    print(f'processing {user_id}:{task_id}')
    try:
        metadata_file = f"metadata_files\\{user_id}-{task_id}.json"
        if not os.path.exists(metadata_file) or os.path.getsize(metadata_file) == 0:
            simulation = download_simulation(user_id, task_id)
            if not simulation:
                return
            metadata_json = simulation_metadata(simulation).json()
            print(metadata_json)
            # Open the file in write mode ('w') and save the string to it
            with open(metadata_file, 'w+') as file:
                file.write(metadata_json)
        else:
            with open(metadata_file, 'r') as f:
                metadata_json = f.read()

        writer.writerow([
            task_id
            , user_id
            , node_size
            , storage_size
            , task_start_time
            , solver_start_time
            , solver_end_time
            , task_end_time
            , num_of_gpu
            , worker
            , gpu_type
            , solver_version
            , real_flex_credit
            , real_time_steps
            , metadata_json
        ])
    except Exception as e:
        print(e)



# Write to CSV file
csv_file = "tidy3d_ml_training.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow([
        "task_id"
        , "user_id"
        , "node_size"
        , "storage_size"
        , "task_start_time"
        , "solver_start_time"
        , "solver_end_time"
        , "task_end_time"
        , "num_of_gpu"
        , "worker"
        , "gpu_type"
        , "solver_version"
        , "real_flex_credit"
        , "real_time_steps"
        , "metadata_json"
    ])
    # Write the data
    for item in result:
        process(writer, item)
        file.flush()

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Submit all items for processing
    futures = [executor.submit(process, writer, item) for item in result]

    for future in concurrent.futures.as_completed(futures):
        try:
            # Get the result of the processing (if any)
            future.result()
        except Exception as e:
            print(f"An error occurred: {e}")

    print("All items have been processed.")