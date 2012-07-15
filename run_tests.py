#!/usr/bin/env python
import unittest
from log import logger

def main():
    # no log messages
    logger.setLevel(1000000000000)

    loader = unittest.TestLoader()
    suite = loader.discover(".", "*_test.py")
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(suite)

if __name__ == '__main__':
    main()