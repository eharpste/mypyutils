import os

def uopen(file, mode='r', unique=False, pad_str='1',
    buffering=-1, encoding=None, errors=None, 
    newline=None, closefd=True, opener=None):
    
    if unique and ('w' in mode or 'x' in mode):
        while(os.path.isfile(file)):
            sp = os.path.splitext(file)
            file = sp[0]+pad_str+sp[1]

    return open(file,mode=mode,buffering=buffering,encoding=encoding,errors=errors,newline=newline,closefd=closefd,opener=opener)

def dir_stream(directory, filter_func = None,
    buffering=-1, encoding=None, errors=None, 
    newline=None, closefd=True, opener=None):

    for fn in filter(filter_func, [f for f in os.listdir(directory) if os.path.isfile(f)]):
        with open(fn,mode='r',buffering=buffering, encoding=encoding, errors=errors, 
                newline=newline, closefd=closefd, opener=opener) as in_f:
            for line in in_f:
                yield line