import os
import sys
import unittest
import unittest.mock
import io

class Test(unittest.TestCase):

    def get_dir(folder_name):
        cwd = os.getcwd()
        basepath = ""
        while True:
            if os.path.exists(folder_name):
                break
            os.chdir("..")
            basepath = os.path.join(basepath, "..")
        os.chdir(cwd)
        if not basepath in sys.path:
            sys.path.insert(0, basepath)

    get_dir("cleaner")
    get_dir("fetcher")

    from cleaner.Cleaner import DataCleaner
    from fetcher.Fetcher import DataFetcher

    cleaner = DataCleaner()
    fetcher = DataFetcher()

    # Tests fetch_a_stock in Fetcher class so it successfully fetches data for GOOG
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_fetcher(self, mock_stdout):
        self.fetcher.fetch_a_stock('GOOG')
        self.assertEqual('Fetched data for GOOG\n', mock_stdout.getvalue(),'Failed when fetching data')
    
    # Tests clean_a_stock in Cleaner class so it successfully cleans data for GOOG
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_cleaner(self, mock_stdout):
        self.cleaner.clean_a_stock('GOOG')
        self.assertEqual('Cleaning data for GOOG\n', mock_stdout.getvalue(), 'Failed when cleaning data')

if __name__ == '__main__':
    unittest.main()
