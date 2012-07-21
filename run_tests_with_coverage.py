#!/usr/bin/env python
import sys
import unittest
from coverage import coverage as Coverage
from log import logger


def main():
    coverage = Coverage()
    coverage.start()

    # no log messages
    logger.setLevel(1000000000000)

    loader = unittest.TestLoader()
    suite = loader.discover(".", "*_test.py")
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(suite)

    coverage.stop()
    coverage.report(file=sys.stdout)
    #coverage.html_report(directory='coverage_report')

if __name__ == '__main__':
    main()
