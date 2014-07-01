#
# custom pymongo encoders for 
# non bsonifyable data formats 
# 1st exmaple was python set.
# 
# see: http://api.mongodb.org/python/current/examples/custom_type.html
#
# khz June / 2014
#
def encode_set(val):
    return list(val)

def decode_set(val):
    return set(val)

