"""Regression testing framework
This module will search for scripts in the same directory named
test_*.py.  Each such script should be a test suite that tests a
module through PyUnit. This script will aggregate all
found test suites into one big test suite and run them all at once.
"""

# Author: Mark Pilgrim
# Modified by Ole Nielsen

import unittest
import os
import sys
import tempfile
import time

# List files that should be excluded from the testing process.
# E.g. if they are known to fail and under development
exclude_files = []

# Directories that should not be searched for test files.
exclude_dirs = ['.svn',          # subversion
                'props', 'wcprops', 'prop-base', 'text-base', 'tmp']


##
# @brief Get 'test_*.py' files and paths to directories.
# @param path Path to directory to start walk in.
# @return A tuple (<files>, <dirs>).
# @note Don't include any files in and below forbidden directories.
def get_test_files(path):
    walk = os.walk(path)

    test_files = []
    path_files = []

    for (dirpath, dirnames, filenames) in walk:
        # exclude forbidden directories
        for e_dir in exclude_dirs:
            try:
                dirnames.remove(e_dir)
            except ValueError:
                pass

        # check for test_*.py files
        for filename in filenames:
            if filename.startswith('test_') and filename.endswith('.py'):
                test_files.append(filename)
                if dirpath not in path_files:
                    path_files.append(dirpath)

    return test_files, path_files


def regressionTest(test_verbose=False):
    # start off with where we are
    path = os.getcwd()
    print
    print 'Testing path: %s' % path



    # get all test_*.py and enclosing directories
    test_files, path_files = get_test_files(path)
    path_files.sort()

    files = [x for x in test_files if not x == 'test_all.py']
    files.sort()        # Ensure same order on all platforms


    print 'Files being tested:'
    for file in files:
        print file
    print

    # update system path with found paths
    for path in path_files:
        sys.path.append(path)
   
    # exclude files that we can't handle 
    for file in exclude_files:
        print 'WARNING: File '+ file + ' to be excluded from testing'
        try:
            files.remove(file)
        except ValueError, e:
            msg = 'File "%s" was not found in test suite.\n' % file
            msg += 'Original error is "%s"\n' % e
            msg += 'Perhaps it should be removed from exclude list?'
            raise Exception, msg

    # import all test_*.py files
    # NOTE: This implies that test_*.py files MUST HAVE UNIQUE NAMES!
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, files)
    modules = map(__import__, moduleNames)

    # Fix up the system path
    for file in path_files:
        sys.path.remove(file)

    # bundle up all the tests
    load = unittest.defaultTestLoader.loadTestsFromModule
    testCaseClasses = map(load, modules)

    if test_verbose is True:
        # Test the code by setting verbose to True.
        # The test cases have to be set up for this to work.
        # See test data manager for an example.
        for test_suite in testCaseClasses:
            for tests in test_suite._tests:
                # tests is of class TestSuite
                if len(tests._tests) > 1:
                    # these are the test functions
                    try:
                        # Calls class method set_verbose in test case classes
                        tests._tests[0].set_verbose()
                    except:
                        pass                # No all classes have set_verbose

    return unittest.TestSuite(testCaseClasses)


##
# @brief Check that the environment is sane.
# @note Stops here if there is an error.
def check_aim_import():
    try:
        # importing something that loads quickly
        import aim
    except ImportError:
        print "Python cannot import aim module."
        print "Check you have followed all steps of its installation."
        import sys
        sys.exit()


if __name__ == '__main__':
    check_aim_import()

    print 'Run tests'
    suite = regressionTest(test_verbose=False)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

