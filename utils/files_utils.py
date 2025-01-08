

def read_file(file_path):
    # 读取文件内容
    with open(file_path, 'rb') as file:
        file_content = file.read()
    return file_content