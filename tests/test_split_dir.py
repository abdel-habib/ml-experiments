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

        self.assertIsNotNone(classes, f"Splitting test failed: {classes}")

        dataset2 = Dataset(
            dataset_path=r'..\\dev\\dataset', 
            csv_path=r'..\\dev\\test.csv',
            output_directory=None,
            output_format="df")

        df, x_col, y_col = dataset2.split_to_df()

        self.assertIsNotNone(df, "DF Splitting test failed")
        self.assertIsNotNone(x_col, f"Splitting test {x_col} failed")
        self.assertIsNotNone(y_col, f"Splitting test {y_col} failed")


if __name__ == "__main__":
    unittest.main()