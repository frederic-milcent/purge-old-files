from datetime import timedelta

from purge_old_files.filters import age, glob, negate
from purge_old_files.finder import File

from tests.helpers import make_test_files_hierarchy


def test_age(tmpdir):
    make_test_files_hierarchy(tmpdir)

    mtime_ge_2_days = age(timedelta(2))
    assert mtime_ge_2_days(File(str(tmpdir.join('foo/1'))))
    assert mtime_ge_2_days(File(str(tmpdir.join('foo/2'))))
    assert mtime_ge_2_days(File(str(tmpdir.join('foo/bar/baz'))))

    mtime_ge_20_days = age(timedelta(20))
    assert not mtime_ge_20_days(File(str(tmpdir.join('foo/1'))))
    assert mtime_ge_20_days(File(str(tmpdir.join('foo/2'))))
    assert mtime_ge_20_days(File(str(tmpdir.join('foo/bar/baz'))))

    mtime_ge_30_days = age(timedelta(30))
    assert not mtime_ge_30_days(File(str(tmpdir.join('foo/1'))))
    assert mtime_ge_30_days(File(str(tmpdir.join('foo/2'))))
    assert mtime_ge_30_days(File(str(tmpdir.join('foo/bar/baz'))))

    mtime_ge_90_days = age(timedelta(90))
    assert not mtime_ge_90_days(File(str(tmpdir.join('foo/1'))))
    assert not mtime_ge_90_days(File(str(tmpdir.join('foo/2'))))
    assert mtime_ge_90_days(File(str(tmpdir.join('foo/bar/baz'))))

    mtime_ge_2_years = age(timedelta(730))
    assert not mtime_ge_2_years(File(str(tmpdir.join('foo/1'))))
    assert not mtime_ge_2_years(File(str(tmpdir.join('foo/2'))))
    assert not mtime_ge_2_years(File(str(tmpdir.join('foo/bar/baz'))))


def test_glob():
    glob_log_ext = glob('*.log')
    assert glob_log_ext(File('foo.log'))
    assert not glob_log_ext(File('bar'))

    glob_date = glob('[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
    assert glob_date(File('20171015'))
    assert not glob_date(File('a20171015'))
    assert not glob_date(File('foo'))


def test_negate():
    not_glob_log = negate(glob('*.log'))
    assert not not_glob_log(File('foo.log'))
    assert not_glob_log(File('bar'))
