import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dupfinder import FileHashInfo, generate_file_hashes, find_duplicate_files


def create_test_files_info():
    return [
        FileHashInfo(0, 'file/path/no/dup'),
        FileHashInfo(1, 'file/path/dup1'),
        FileHashInfo(1, 'file/path/dup2'),
    ]


def test__find_duplicate_files__no_false_positives():
    test_files_info = create_test_files_info()

    found_duplicates = find_duplicate_files(test_files_info)

    for duplicate_group in found_duplicates:
        assert 'file/path/no/dup' not in duplicate_group


def test__find_duplicate_files__finds_duplicates():
    test_files_info = create_test_files_info()

    found_duplicates = find_duplicate_files(test_files_info)

    found = False
    for duplicate_group in found_duplicates:
        if duplicate_group == ['file/path/dup1', 'file/path/dup2']:
            found = True
            break

    assert found, 'Duplicate files not found'


class FileBytesAndHash:
    def __init__(self, bytes_content):
        self.bytes_content = bytes_content
        self.hash = hash(bytes_content)


fake_file_bytes = {
    '/path/one': FileBytesAndHash(b'path one content'),
    '/path/two': FileBytesAndHash(b'path two content'),
    '/path/three': FileBytesAndHash(b'path three content'),
}


def fake__get_file_bytes(path):
    return fake_file_bytes[path].bytes_content


def test__generate_file_hashes():
    generated_hashes = generate_file_hashes(fake_file_bytes.keys(), fake__get_file_bytes)

    for gen_hash_info in generated_hashes:
        assert gen_hash_info.hash == fake_file_bytes[gen_hash_info.path].hash