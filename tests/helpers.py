from datetime import datetime, timedelta
from os import utime


def make_test_files_hierarchy(tmpdir):
    # pylint: disable=blacklisted-name
    now = datetime.now()
    one_week_ago = (now - timedelta(days=7)).timestamp()
    one_month_ago = (now - timedelta(days=30)).timestamp()
    one_year_ago = (now - timedelta(days=365)).timestamp()

    foo = tmpdir.mkdir('foo')
    foo_1 = foo.join('1')
    foo_1.write('1')
    utime(str(foo_1), (one_week_ago, one_week_ago))

    foo_2 = foo.join('2')
    foo_2.write('2')
    utime(str(foo_2), (one_month_ago, one_month_ago))

    baz = foo.mkdir('bar').join('baz')
    baz.write('baz')
    utime(str(baz), (one_year_ago, one_year_ago))

    foobar = tmpdir.mkdir('foobar')
    foobar_1 = foobar.join('1')
    foobar_1.write('1')
    utime(str(foobar_1), (one_month_ago, one_month_ago))
