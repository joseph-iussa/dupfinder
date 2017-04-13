import os

from collections import namedtuple
from itertools import groupby
from pathlib import Path


FileHashInfo = namedtuple('FileHashInfo', ['hash', 'path'])


def get_absolute_root_paths(root_paths):
    try:
        return [str(Path(path).resolve()) for path in root_paths]
    except FileNotFoundError:
        raise


def get_absolute_file_paths(root_paths):
    abs_paths = set()

    for root_path in root_paths:
        for dirpath, dirnames, filenames in os.walk(root_path):
            for name in filenames:
                abs_paths.add(os.path.abspath(os.path.join(dirpath, name)))

    return list(abs_paths)


def get_file_bytes(path):
    with open(path, 'rb') as file:
        return file.read()


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