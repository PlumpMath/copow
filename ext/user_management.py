#
# copow user password encryption
# created by khz (2014)
# you can use these functions in your user managent controllers.
# 
# taken from Stackoverflow:
# see: 
#   http://stackoverflow.com/questions/5293959/creating-a-salt-in-python
#   http://stackoverflow.com/questions/1183161/to-sha512-hash-a-password-in-mysql-database-by-python
#
import random
import hashlib
from #APPNAME.models.user import User
from #APPNAME.config.settings import base

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def set_password(raw_password):
    salt = ''.join(random.choice(ALPHABET) for i in range(16))
    hexhash = hashlib.sha512(raw_password.encode(base["default_encoding"]) + salt.encode(base["default_encoding"])).hexdigest()
    return (hexhash ,salt)


def check_password(raw_password, check_hexhash, salt):
    hexhash = hashlib.sha512(raw_password + salt).hexdigest()
    if hexhash == check_hexhash:
       return True
    else:
        return False

def get_salt_and_hash(user_id=None, loginname=None):
    u = User()
    if user_id:
        u = find_by("_id", user_id)
        return (u.salt, u.hexhash)

    if loginname:
        u = find_by("loginname", loginname)
        return (u.salt, u.hexhash)