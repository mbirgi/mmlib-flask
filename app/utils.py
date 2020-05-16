import os

def debug(label, arg):
    if os.getenv('MMLIB_DEV_MODE'):
        print(f"{label} = {arg}")
