import os
import sys
from ctypes import *
from contextlib import contextmanager

# ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

# def py_error_handler(filename, line, function, err, fmt):
#     pass

# c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

# @contextmanager
# def noalsaerr():
#     asound = cdll.LoadLibrary('libasound.so')
#     asound.snd_lib_error_set_handler(c_error_handler)
#     yield
#     asound.snd_lib_error_set_handler(None)

# ... Another trick to have a clean console (This silence pyaudio trying to connect to Jack server and some bad configuration from /usr/share/alsa/alsa.conf)    
# @contextmanager
def noalsaerr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)