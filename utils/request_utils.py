import requests
from requests.auth import HTTPBasicAuth
from utils import files_utils
import json
from config import config

username = config['username']
password = config['password']
base_url = config['ip'] + ":" + config['port']


def create_kb(filepaths,index_name,max_length,overlap_length,segment_id):
    url = f'{base_url}/vector_stores/create'
    files = []
    for f in filepaths:
        filename = f.split('/')[-1]
        filetype = filename.split('.')[-1]
        file_base64 = files_utils.file_to_base64(f)
        language = 'cn'
        file_info = {"file_name":filename,"file_base64":file_base64,"file_type":filetype,"language":language}
        files.append(file_info)
    
    data = {
      "files":files,
      "name":index_name,
      "chunking_strategy":{"chunk_type":1,"max_tokens":max_length,"overlap":overlap_length,"separator":segment_id}
    }
    
    response = requests.post(url, auth=HTTPBasicAuth(username, password), data=json.dumps(data))

    return response


def upload_files(filepaths,index_id,max_length,overlap_length,segment_id):
    url = f"{base_url}/vector_stores/{index_id}/upload"
    files = []
    for f in filepaths:
        filename = f.split('/')[-1]
        filetype = filename.split('.')[-1]
        file_base64 = files_utils.file_to_base64(f)
        language = 'cn'
        file_info = {"file_name":filename,"file_base64":file_base64,"file_type":filetype,"language":language}
        files.append(file_info)
    
    data = {
      "files":files,
      "chunking_strategy":{"chunk_type":1,"max_tokens":max_length,"overlap":overlap_length,"separator":segment_id}
    }
    
    response = requests.post(url, auth=HTTPBasicAuth(username, password), data=json.dumps(data))

    return response


def reload_files(reload_index_id):
    url = f"{base_url}/vector_stores/{reload_index_id}/files"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    return response


def delete_file(reload_index_id, file_name):
    url = f"{base_url}/vector_stores/{reload_index_id}/files/{file_name}"
    response = requests.delete(url, auth=HTTPBasicAuth(username, password))
    return response



