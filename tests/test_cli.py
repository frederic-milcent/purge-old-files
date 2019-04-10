from os.path import join
from glob import glob
import logging
import logging.handlers

from purge_old_files import cli, finder

import pytest

from tests.helpers import make_test_files_hierarchy


@pytest.mark.parametrize(
    'arguments, directories, expected_remaining, log_level, log_handler_class',
    (
        (
            ['--dry-run', '10s'],
            ['foo'],
            ['foo/1', 'foo/2', 'foo/bar/baz'],
            logging.INFO,
            logging.StreamHandler,
        ),
        (
            ['-Ds', '1d'],
            ['foo'],
            [],
            logging.DEBUG,
            logging.handlers.SysLogHandler,
        ),
        (
            ['3M'],
            ['foo'],
            ['foo/1', 'foo/2'],
            logging.INFO,
            logging.StreamHandler,
        ),
        (
            ['--include', '[0-9]', '10d'],
            ['foo'],
            ['foo/1', 'foo/bar/baz'],
            logging.INFO,
            logging.StreamHandler,
        ),
        (
            ['--exclude', '[0-9]', '10d'],
            ['foo'],
            ['foo/1', 'foo/2'],
            logging.INFO,
            logging.StreamHandler,
        ),
        (
            ['--include', '[0-9]', '--exclude', '2', '-q', '10d'],
            ['foo'],
            ['foo/1', 'foo/2', 'foo/bar/baz'],
            logging.WARNING,
            logging.StreamHandler
        ),
        (
            ['10d'],
            ['foo', 'foobar'],
            ['foo/1'],
            logging.INFO,
            logging.StreamHandler,
        ),
        (
            ['10d'],
            ['foo*'],
            ['foo/1'],
            logging.INFO,
            logging.StreamHandler,
        ),
    ),
)
def test(  # pylint: disable=too-many-arguments
        arguments, directories, expected_remaining, log_level,
        log_handler_class, tmpdir):
    # Prepare the environment
    make_test_files_hierarchy(tmpdir)
    str_tmpdir = str(tmpdir)
    root_logger = logging.getLogger()
    # Call the CLI
    absolute_directories = [
        join(str_tmpdir, directory) for directory in directories]
    cli.main(arguments + absolute_directories)
    # Ensure results are consistent
    remaining_files = sorted(
        file_
        for pattern in absolute_directories
        for directory in glob(pattern)
        for file_ in finder.find(directory))
    assert remaining_files == [
        finder.File(join(str_tmpdir, path)) for path in expected_remaining]
    # Ensure verbosity control works as expected
    assert root_logger.level == log_level
    # Ensure the request log handler is used
    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0], log_handler_class)
    # Reset the root logger
    root_logger.handlers = []
