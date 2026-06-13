import functions_framework

@functions_framework.cloud_event
def process_s3_event(cloud_event):
    data = cloud_event.data
    bucket = data['bucket']
    name = data['name']
    
    print(f"File processed in GCP! Bucket: {bucket}, File: {name}")
