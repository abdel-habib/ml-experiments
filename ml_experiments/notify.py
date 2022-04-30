import time
import socket
import functools
import re
import yagmail
from loguru import logger
from datetime import datetime


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
REGEX = "[^@]+@[^@]+\.[^@]+"

def notify_email(recipient_emails: list, sender_email: str):

    if sender_email is None or not isinstance(sender_email, str):
        raise Exception('You must provide a single sender email as a string')

    if not re.fullmatch(REGEX, sender_email):
        raise Exception(f'{sender_email} is not a valid email format.')

    if(not isinstance(recipient_emails, list)):
        recipient_emails = [recipient_emails]

    for _, email in enumerate(recipient_emails):
        print(email)
        if not re.fullmatch(REGEX, email):
            raise Exception(f'{email} is not a valid email format.')

    yag  = yagmail.SMTP(sender_email)

    def decorator_func(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):

            machine = socket.gethostname()
            func_name = func.__name__
            start_time = datetime.now().strftime(DATE_FORMAT)
            # email_msg = MIMEMultipart()

            try:
                func(*args, **kwargs)
                end_time = datetime.now().strftime(DATE_FORMAT)

                yag.send(
                    recipient_emails,"Subject Of Mail","Content Of Mail"
                )

            except Exception as e: 
                logger.error('Failed to upload to ftp: '+ str(e))
            
        return wrapper_func
    return decorator_func


@notify_email(recipient_emails=['abdalrhmanusama1@gmail.com'], sender_email='abdalrhmanusama1@gmail.com')
def daily_backup():

    time.sleep(3)
    print('Daily backup job has finished.')   
    # raise Exception("testing logger")
    return 3

daily_backup()
