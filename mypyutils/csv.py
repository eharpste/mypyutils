import csv

class Row:
    def __init__(self,row,header,delim):
        self.row = {header[i]:None if i >= len(row) else row[i] for i in range(len(header))}
        self.delim = delim
        self.header = header

    def __getitem__(self,key):
        if isinstance(key,int):
            return self.row[self.header[key]]
        else:
            try:
                return self.row[key]    
            except KeyError :
                print("'"+key+"' not found in header list:\n"+'\n'.join(self.header))
                raise

    def __setitem__(self,key,value):
        if isinstance(key,int):
            self.row[self.header[key]] = value
        else:
            self.row[key] = value

    def __len__(self):
        return len(self.row)

    def __str__(self):
        return self.delim.join([str(self.row[k]) for k in self.header])

    def str_header(self):
        return self.delim.join(self.header)

def csv_header(f_name,delimiter='\t',encoding=None):
     with open(f_name,mode='r',encoding=encoding) as f:
        c = csv.reader(f,delimiter = delimiter)
        for row in c:
            return row

def csv_stream(f_name,delimiter='\t',encoding=None):
    with open(f_name,mode='r',encoding=encoding) as f:
        c = csv.reader(f,delimiter = delimiter)
        h = None
        for row in c:
            if h is None:
                h = [v.strip() for v in row]
                continue
            if len(row) == 0:
                continue
            else:
                yield Row(row,h,delimiter)
        raise StopIteration
