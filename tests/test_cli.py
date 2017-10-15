from os.path import join

from purge_old_files import cli, finder

import pytest

from tests.helpers import make_test_files_hierarchy


@pytest.mark.parametrize('arguments, remaining', (
    (['--dry-run', '10s'], ['foo/1', 'foo/2', 'foo/bar/baz']),
    (['1d'], []),
    (['3M'], ['foo/1', 'foo/2']),
    (['--include', '[0-9]', '10d'], ['foo/1', 'foo/bar/baz']),
    (['--exclude', '[0-9]', '10d'], ['foo/1', 'foo/2']),
    (
        ['--include', '[0-9]', '--exclude', '2', '10d'],
        ['foo/1', 'foo/2', 'foo/bar/baz'],
    ),
))
def test(arguments, remaining, tmpdir):
    make_test_files_hierarchy(tmpdir)
    str_tmpdir = str(tmpdir)
    cli.main(arguments + [str_tmpdir])
    assert sorted(finder.find(str_tmpdir)) == [
        finder.File(join(str_tmpdir, path)) for path in remaining]
