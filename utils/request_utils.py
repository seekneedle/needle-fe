import requests
from requests.auth import HTTPBasicAuth
from utils import files_utils
from config import config
from utils.security import decrypt
import time

username = config['username']
password = decrypt(config['password'])
base_url = 'http://' + config['ip'] + ":" + str(config['port'])


def create_kb(uploaded_files,index_name,max_length,overlap_length,segment_id):
    url = f'{base_url}/vector_store/create'
    files = []
    for f in uploaded_files:
        files.append(('files', (f.name, f.getbuffer())))
    
    data = {
        "name":index_name,
        "chunk_size": max_length,
        "overlap_size": overlap_length
    }
    
    response = requests.post(url, auth=HTTPBasicAuth(username, password), data=data, files=files)

    task_id = response.json()['data']['task_id']

    status_url = f'{base_url}/vector_store/task_status/{task_id}'

    counter = 0

    while counter < 50:
        time.sleep(6)

        status_response = requests.get(status_url, auth=HTTPBasicAuth(username, password))

        status_data = status_response.json()['data']

        if status_data['status'] == 'COMPLETED' or status_data['status'] == 'FAILED':
            return status_response

    return response


def upload_files(uploaded_files,index_id,max_length,overlap_length,segment_id):
    url = f'{base_url}/vector_store/file/add'

    files = []
    for f in uploaded_files:
        files.append(('files', (f.name, f.getbuffer())))

    data = {
        "id": index_id
    }

    response = requests.post(url, auth=HTTPBasicAuth(username, password), data=data, files=files)

    task_id = response.json()['data']['task_id']

    status_url = f'{base_url}/vector_store/task_status/{task_id}'

    counter = 0

    while counter < 50:
        time.sleep(6)

        status_response = requests.get(status_url, auth=HTTPBasicAuth(username, password))

        status_data = status_response.json()['data']

        if status_data['status'] == 'COMPLETED' or status_data['status'] == 'FAILED':
            return status_response

    return response


def reload_files(reload_index_id):
    url = f"{base_url}/vector_store/file/list/{reload_index_id}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    return response


def delete_file(reload_index_id, file_id):
    data = {
        "id": reload_index_id,
        "file_ids": [file_id]
    }
    url = f"{base_url}/vector_store/file/delete"
    response = requests.post(url, auth=HTTPBasicAuth(username, password), json=data)
    return response


def get_store_list():
    url = f"{base_url}/vector_store/list"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    return response
