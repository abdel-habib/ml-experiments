# ML Experiments

This package is under development.


## Installation

```python
pip install ml-experiments
```

### Notification
```python
from ml_experiments.notify import notify_desktop, notify_email

@notify_desktop(title='Testing Completed!')
  def train():
    // .. some training code ..
    return {"loss": 5}

@notify_email(recipient_emails=['emai1@email.com'], sender_email=['emai2@email.com','emai3@email.com'])
  def train():
    // .. some training code ..
    return {"loss": 5}
```

### Dataset Splitting
```python
from ml_experiments.data_prep import Dataset

dataset = Dataset(
  dataset_path=r'..\\dev\\dataset', 
  csv_path=r'..\\dev\\test.csv',
  output_directory=r'..\\dev\\out',
  # output_directory=None, 
  output_format="dir")

dataset.split_to_directory()

```

### Running Tests
```python
cd tests
python3 test_filename.py
```
