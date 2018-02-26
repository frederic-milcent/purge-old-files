from os.path import join
import logging

from purge_old_files import cli, finder

import pytest

from tests.helpers import make_test_files_hierarchy


@pytest.mark.parametrize('arguments, remaining, log_level', (
    (['--dry-run', '10s'], ['foo/1', 'foo/2', 'foo/bar/baz'], logging.INFO),
    (['-D', '1d'], [], logging.DEBUG),
    (['3M'], ['foo/1', 'foo/2'], logging.INFO),
    (['--include', '[0-9]', '10d'], ['foo/1', 'foo/bar/baz'], logging.INFO),
    (['--exclude', '[0-9]', '10d'], ['foo/1', 'foo/2'], logging.INFO),
    (
        ['--include', '[0-9]', '--exclude', '2', '-q', '10d'],
        ['foo/1', 'foo/2', 'foo/bar/baz'],
        logging.WARNING,
    ),
))
def test(arguments, remaining, log_level, tmpdir):
    # Prepare the environment
    make_test_files_hierarchy(tmpdir)
    str_tmpdir = str(tmpdir)
    # Call the CLI
    cli.main(arguments + [str_tmpdir])
    # Ensure results are consistent
    assert sorted(finder.find(str_tmpdir)) == [
        finder.File(join(str_tmpdir, path)) for path in remaining]
    # Ensure verbosity control works as expected
    assert logging.getLogger().level == log_level
