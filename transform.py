# Description: This file contains functions that are used to transform data from one format to another.


def json_extract(obj, key):

    arr = []
    
    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k,v in obj.items():
                if k == key:
                    arr.append(v)
                elif isinstance(v,(dict,list)):
                    extract(v, arr, key)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    values = extract(obj, arr, key)
    return values

def create_mapped_dict(item1, item2):
    item_dict = dict(map(lambda i,j: (i,j),item1, item2))
    return item_dict