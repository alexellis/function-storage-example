from minio import Minio
import requests
import json
import uuid
import os

def handle(st):
    req = json.loads(st)

    mc = Minio(os.environ['minio_hostname'],
                  access_key=os.environ['minio_access_key'],
                  secret_key=os.environ['minio_secret_key'],
                  secure=False)

    names = []
    source_bucket = "incoming"
    dest_bucket = "processed"

    for file_name in req:
        names.append(convert_push(source_bucket, dest_bucket, file_name, mc))

    print(json.dumps(names))

def convert_push(source_bucket, dest_bucket, file_name, mc):
    mc.fget_object(source_bucket, file_name, "/tmp/" + file_name)

    f = open("/tmp/" + file_name, "rb")
    input_image = f.read()

    # download file
    r = requests.post("http://gateway:8080/function/convertbw", input_image)

    # write to temporary file
    dest_file_name = get_temp_file()
    f = open("/tmp/" + dest_file_name, "wb")
    f.write(r.content)
    f.close()

    # sync to Minio
    mc.fput_object(dest_bucket, dest_file_name, "/tmp/"+dest_file_name)

    return dest_file_name

def get_temp_file():
    uuid_value = str(uuid.uuid4())
    return uuid_value
