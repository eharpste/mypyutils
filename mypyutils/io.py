from datetime import datetime
import os


def uopen(file, mode='r', unique=False, pad_str=None,
          buffering=-1, encoding=None, errors=None,
          newline=None, closefd=True, opener=None):
    """
    Open a new file reference with option to force unique file names.

    The parameters gnerally follow the same function as their counterparts in
    the standard open function with the exception of unique, which flags
    whether a unique file should be created in w or x mode, and pad_str, which
    sets what string to use to pad the unique file name. If not pad_str is
    provided the current date time is used.
    """
    if unique and ('w' in mode or 'x' in mode):
        if(os.path.isfile(file)):
            if pad_str is None:
                sp = os.path.splitext(file)
                file = sp[0] + ' - ' + datetime.now().isoformat(' ') + sp[1]
            else:
                while(os.path.isfile(file)):
                    sp = os.path.splitext(file)
                    file = sp[0] + pad_str + sp[1]

    return open(file, mode=mode, buffering=buffering, encoding=encoding,
                errors=errors, newline=newline, closefd=closefd, opener=opener)


def dir_stream(directory, filter_func=None,
               buffering=-1, encoding=None, errors=None,
               newline=None, closefd=True, opener=None):

    for fn in filter(filter_func,
                     [f for f in os.listdir(directory) if os.path.isfile(f)]):
        with open(fn, mode='r', buffering=buffering, encoding=encoding,
                  errors=errors, newline=newline, closefd=closefd,
                  opener=opener) as in_f:
            for line in in_f:
                yield line
