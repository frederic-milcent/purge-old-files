from datetime import timedelta
import os

from purge_old_files.finder import find, File
from purge_old_files.filters import age, glob

from tests.helpers import make_test_files_hierarchy


def test_find(tmpdir):
    make_test_files_hierarchy(tmpdir)

    # No filtering
    assert sorted(find(str(tmpdir))) == [
        File('%s/foo/1' % tmpdir),
        File('%s/foo/2' % tmpdir),
        File('%s/foo/bar/baz' % tmpdir),
        File('%s/foobar/1' % tmpdir),
    ]

    # Test filtering based on time
    assert find(str(tmpdir), [age(timedelta(days=90))]) == [
        File('%s/foo/bar/baz' % tmpdir),
    ]

    # Test filtering based on glob pattern
    assert sorted(find(str(tmpdir), [glob('[0-9]')])) == [
        File('%s/foo/1' % tmpdir),
        File('%s/foo/2' % tmpdir),
        File('%s/foobar/1' % tmpdir),
    ]

    # Test with a mix of filters
    assert find(str(tmpdir), [glob('[0-9]'), age(timedelta(days=8))]) == [
        File('%s/foo/2' % tmpdir),
        File('%s/foobar/1' % tmpdir),
    ]


def test_file_stat(tmpdir):
    # Create an empty file
    file_path = tmpdir.join('file')
    file_path.write('')
    # Create a symlink to it
    link_path = tmpdir.join('link')
    os.symlink(str(file_path), str(link_path))
    # Ensure they don't return the same stat values
    assert File(str(file_path)).stat != File(str(link_path)).stat
