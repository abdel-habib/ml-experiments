import sys
sys.path.append("..\\")
import unittest

from ml_experiments.data_prep import Dataset

class TestSplitToDir(unittest.TestCase):
    def test(self):
        dataset = Dataset(
            dataset_path=r'..\\dev\\dataset', 
            csv_path=r'..\\dev\\test.csv',
            output_directory=r'..\\dev\\out',
            # output_directory=None, 
            output_format="dir")

        dataset.split_to_directory()
        classes = dataset.get_classes()

        self.assertIsNotNone(classes, "Slitting test failed")

if __name__ == "__main__":
    unittest.main()