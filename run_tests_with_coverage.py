#!/usr/bin/env python
import sys
import os
import re
import unittest
from coverage import coverage as Coverage
from log import logger
import argparse

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description="""
        This script runs all test and show coverage with Coverage""")
    arg_parser.add_argument(
        '-hr', '--html-report',
        help='Directory save htmlreport to'
    )
    args = arg_parser.parse_args()


def main():
    list_of_test_files = list()
    for directory in os.walk('.'):
        for filename in directory[2]:
            if re.search(".*_tests?\.py", filename):
                list_of_test_files.append(filename)
    list_of_test_files.append('config_testing.py')
    coverage = Coverage(omit=list_of_test_files)
    list_of_test_files.pop()
    coverage.start()

    # no log messages
    logger.setLevel(1000000000000)

    loader = unittest.TestLoader()
    suite = loader.discover('.', '*_test.py')
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(suite)

    coverage.stop()
    coverage.report(file=sys.stdout)

    if args.html_report:
        coverage.html_report(directory=args.html_report)
    print(test_result)


if __name__ == '__main__':
    main()
