from datetime import timedelta

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
    ]

    # Test filtering based on time
    assert find(str(tmpdir), [age(timedelta(days=90))]) == [
        File('%s/foo/bar/baz' % tmpdir),
    ]

    # Test filtering based on glob pattern
    assert sorted(find(str(tmpdir), [glob('[0-9]')])) == [
        File('%s/foo/1' % tmpdir),
        File('%s/foo/2' % tmpdir),
    ]

    # Test with a mix of filters
    assert find(str(tmpdir), [glob('[0-9]'), age(timedelta(days=8))]) == [
        File('%s/foo/2' % tmpdir),
    ]
