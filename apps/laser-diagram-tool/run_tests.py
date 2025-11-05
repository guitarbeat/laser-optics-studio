import unittest
import sys
import os

if __name__ == '__main__':
    # Add the 'src' directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

    # Now that the path is set, we can import the test
    from tests.test_application import TestHandleTab

    # Create a TestSuite
    suite = unittest.TestSuite()

    # Add tests from the TestHandleTab class
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestHandleTab))

    # Run the tests
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Exit with a non-zero status code if tests fail
    if not result.wasSuccessful():
        sys.exit(1)
