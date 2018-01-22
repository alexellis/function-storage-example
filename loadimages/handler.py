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
    for url in req["urls"]:
        names.append(download_push(url, mc))
    print(json.dumps(names))

def download_push(url, mc):
    # download file
    r = requests.get(url)

    # write to temporary file
    file_name = get_temp_file()
    f = open("/tmp/" + file_name, "wb")
    f.write(r.content)
    f.close()

    # sync to Minio
    mc.fput_object("incoming", file_name, "/tmp/"+file_name)
    return file_name

def get_temp_file():
    uuid_value = str(uuid.uuid4())
    return uuid_value


