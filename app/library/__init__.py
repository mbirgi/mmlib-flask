import os
from .json_library import JSONLibrary

_dev = os.getenv('MMLIB_DEV_MODE')

library = JSONLibrary()
