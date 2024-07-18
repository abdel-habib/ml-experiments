import time
import socket
import functools
import re
import yagmail
import sys
import subprocess
import platform

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
        if not re.fullmatch(REGEX, email):
            raise Exception(f'{email} is not a valid email format.')

    yag  = yagmail.SMTP(sender_email)

    def decorator_func(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):

            machine = socket.gethostname()
            func_name = func.__name__
            start_time = datetime.now().strftime(DATE_FORMAT)

            try:
                value = func(*args, **kwargs)
                end_time = datetime.now().strftime(DATE_FORMAT)

                contents = [
                    f'You are receiving this email as the {func_name} process running on {machine} machine is completed 🚀.',
                    f'This process started at {start_time} and finished successfully at {end_time}.'
                ]

                yag.send(
                    to = recipient_emails,
                    subject = 'Process finished successfully 🚀.',
                    contents = '\n'.join(contents))
                
                return value

            except Exception as e: 
                logger.error('Error occurred during the process: '+ str(e))
                
                end_time = datetime.now().strftime(DATE_FORMAT)

                contents = [
                    f'The error occured at {datetime.now().strftime(DATE_FORMAT)} with an exception "{str(e)}"',
                    f'Your process running on {machine} machine started at {start_time} and failed at {end_time}.'
                ]

                yag.send(
                    to = recipient_emails,
                    subject = 'An error occurred while running your script.',
                    contents = '\n'.join(contents))

                raise e
            
        return wrapper_func
    return decorator_func


def notify_desktop(title: str = "Desktop Notification"):

    def display_notification(text: str, title: str):
        if platform.system() == "Windows":

            try:
                from win10toast import ToastNotifier
            except Exception as e:
                logger.error("Error importing ToastNotifier, please run pip install win10toast")

            toast = ToastNotifier()

            toast.show_toast(
                title=title,
                msg=text,
                icon_path=None,
                duration=7)

            pass

        elif platform.system() == "Linux":
            subprocess.run(["notify-send", title, text])

        elif platform.system() == "Darwin":
            subprocess.run(["sh", "-c", "osascript -e 'display notification \"%s\" with title \"%s\"'" % (text, title)])


    def decorator_func(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):

            machine = socket.gethostname()
            func_name = func.__name__
            start_time = datetime.now().strftime(DATE_FORMAT)

            try:
                value = func(*args, **kwargs)
                end_time = datetime.now().strftime(DATE_FORMAT)

                contents = [
                    f'You are receiving this notification as the {func_name} process running on {machine} machine is completed 🚀.',
                    f'This process started at {start_time} and finished successfully at {end_time}.'
                ]

                display_notification(text='\n'.join(contents), title=title)

                return value
            except Exception as e: 
                logger.error('Error occurred during the process: '+ str(e))
                
                end_time = datetime.now().strftime(DATE_FORMAT)

                contents = [
                    f'An error occurred while running your script.',
                    f'The error occurred at {datetime.now().strftime(DATE_FORMAT)} with an exception "{str(e)}"',
                    f'Your process running on {machine} machine started at {start_time} and failed at {end_time}.'
                ]

                display_notification(text='\n'.join(contents), title=title)

                raise e
            
        return wrapper_func
    return decorator_func