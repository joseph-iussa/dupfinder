from pathlib import Path
from dupfinder.core import get_absolute_file_paths


def test__get_absolute_file_paths__gets_all_paths(tmpdir):
    test_paths = (
        Path(str(tmpdir), 'foo.txt'),
        Path(str(tmpdir), 'sub/foo.txt'),
        Path(str(tmpdir), 'sub/bar.txt'),
        Path(str(tmpdir), 'sub/sub/baz.txt'),
        Path(str(tmpdir), 'sub/sub/box.txt'),
    )
    for path in test_paths:
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        path.touch()
    test_root_paths = (
        str(Path(str(tmpdir), '.').resolve()),
        str(Path(str(tmpdir), 'sub').resolve())
    )

    returned_paths = get_absolute_file_paths(test_root_paths)

    assert all(str(test_path.resolve()) in returned_paths for test_path in test_paths)