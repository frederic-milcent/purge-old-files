from os.path import join
import logging
import logging.handlers

from purge_old_files import cli, finder

import pytest

from tests.helpers import make_test_files_hierarchy


@pytest.mark.parametrize(
    'arguments, remaining, log_level, log_handler_class',
    (
        (
            ['--dry-run', '10s'],
            ['foo/1', 'foo/2', 'foo/bar/baz'],
            logging.INFO,
            logging.StreamHandler,
        ),
        (
            ['-Ds', '1d'],
            [],
            logging.DEBUG,
            logging.handlers.SysLogHandler,
        ),
        (
            ['3M'],
            ['foo/1', 'foo/2'],
            logging.INFO,
            logging.StreamHandler,
        ),
        (
            ['--include', '[0-9]', '10d'],
            ['foo/1', 'foo/bar/baz'],
            logging.INFO,
            logging.StreamHandler,
        ),
        (
            ['--exclude', '[0-9]', '10d'],
            ['foo/1', 'foo/2'],
            logging.INFO,
            logging.StreamHandler,
        ),
        (
            ['--include', '[0-9]', '--exclude', '2', '-q', '10d'],
            ['foo/1', 'foo/2', 'foo/bar/baz'],
            logging.WARNING,
            logging.StreamHandler
        ),
    ),
)
def test(arguments, remaining, log_level, log_handler_class, tmpdir):
    # Prepare the environment
    make_test_files_hierarchy(tmpdir)
    str_tmpdir = str(tmpdir)
    root_logger = logging.getLogger()
    # Call the CLI
    cli.main(arguments + [str_tmpdir])
    # Ensure results are consistent
    assert sorted(finder.find(str_tmpdir)) == [
        finder.File(join(str_tmpdir, path)) for path in remaining]
    # Ensure verbosity control works as expected
    assert root_logger.level == log_level
    # Ensure the request log handler is used
    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0], log_handler_class)
    # Reset the root logger
    root_logger.handlers = []
