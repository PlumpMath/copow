#
# custom pymongo encoders for 
# non bsonifyable data formats 
# 1st exmaple was python set.
# 
# see: http://api.mongodb.org/python/current/examples/custom_type.html
#
# khz June / 2014
#
from bson.objectid import ObjectId

def set_encode_python(val):
    if isinstance(val, str):
        val = val.split(" ")
    return set(val)

def set_encode_json(val):
    return list(val)
    
def set_encode_db(val):
    return list(val)

def set_encode_str(val):
    ostr = ""
    for elem in val:
        ostr += str(elem) + " "
    return ostr

def oid_encode_python(val):
    if isinstance(val, str):
        return ObjectId(val)
    elif isinstance(val,ObjectId):
        return val
    else:
        return ObjectId(str(val))

def oid_encode_json(val):
    return str(val)

def oid_encode_db(val):
    return ObjectId(val)
