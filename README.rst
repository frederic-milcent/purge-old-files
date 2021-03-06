Purge old files
===============

Simple tool to delete old files using a set of contraints.

If ``--include`` if used,
only files matching the provided glob pattern are considered.
This option can be used multiple times.
By default, all files are considered.


Usage
-----

.. code-block:: console

    $ purge-old-files -h
    usage: purge-old-files [-h] [--debug | --quiet] [--syslog] [--dry-run]
                           [--include PATTERN] [--exclude PATTERN]
                           MIN_AGE [DIRECTORY [DIRECTORY ...]]

    positional arguments:
      MIN_AGE               Minimum age of files
      DIRECTORY             Directory or glob pattern to be scanned (multiple
                            directories can be provided)

    optional arguments:
      -h, --help            show this help message and exit
      --debug, -D           Show debug messages
      --quiet, -q           Only show warning messages
      --syslog, -s          Send log messages to /dev/log instead of stdout
      --dry-run, -d         Show which files should be deleted
      --include PATTERN, -i PATTERN
                            Include only files matching pattern
      --exclude PATTERN, -e PATTERN
                            Exclude files matching pattern

    # Purge *.log files in /logs when they are older than 3 days
    $ purge-old-files --include '*.log' 3d /logs

    # Delete files from /backup when they are older than 1 week
    $ purge-old-files 1w /backup

    # Show which files from /backup are older than 3 months
    $ purge-old-files --dry-run 3M /backup


File minimum age
----------------

Supported units:

* ``s``: seconds
* ``m``: minutes
* ``h``: hours
* ``d``: days
* ``w``: weeks
* ``M``: months (30 days)
* ``y``: years (365 days)


Installation
------------

.. code-block:: console

    $ pip install purge-old-files


Requirements
------------

* Python 3.x


FAQ
---

* Do you know you can do this with a simple shell script using ``find``?

  Yep. I wrote those for years. They are also painful to maintain.
  And error prone. Feel free to use a shell script. :)
