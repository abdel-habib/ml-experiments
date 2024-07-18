import sys
sys.path.append("..\\")

import unittest
import time
from ml_experiments.models.callbacks.notify import notify_desktop

class TestSenders(unittest.TestCase):
    def test_desktop(self):
        @notify_desktop(title='Testing Completed!')
        def train():
            time.sleep(2)
            return {"loss": 5}
        self.assertEqual(train(), {"loss": 5})


if __name__ == "__main__":
    unittest.main()