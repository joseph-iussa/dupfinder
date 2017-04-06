from collections import namedtuple
from itertools import groupby


FileHashInfo = namedtuple('FileHashInfo', ['hash', 'path'])


def get_file_bytes(path):
    with open(path, 'rb') as file:
        return file.readall()


def generate_file_hashes(paths, file_bytes_provider):
    file_hashes = []
    for path in paths:
        file_hashes.append(FileHashInfo(hash(file_bytes_provider(path)), path))
    return file_hashes


def find_duplicate_files(files_info):
    duplicates = []

    cmpkey = lambda fileinfo: fileinfo.hash
    files_info.sort(key=cmpkey)
    for _, group in groupby(files_info, cmpkey):
        group = list(group)
        if len(group) < 2:
            continue
        duplicates.append([file_info.path for file_info in group])

    duplicates.sort(key=lambda d: d[0])
    return duplicates