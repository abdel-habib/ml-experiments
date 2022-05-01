import sys
sys.path.append("..\\")

import unittest
import time
from ml_experiments.notify import notify_email

class TestSenders(unittest.TestCase):
    def test_email(self):
        @notify_email(recipient_emails=['abdalrhmanusama1@gmail.com'], sender_email='emaildev037@gmail.com')
        def train():
            time.sleep(5)
            return {"loss": 1}
        self.assertEqual(train(), {"loss": 1})


if __name__ == "__main__":
    unittest.main()