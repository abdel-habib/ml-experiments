# ML Experiments

This package is under development.


## Installation

```python
pip3 install ml-experiments --upgrade

# or (if you are not getting the latest version)
pip3 install git+https://github.com/abdalrhmanu/ml-experiments.git --upgrade
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

### Running Tests
```python
cd tests
python3 test_filename.py
```
