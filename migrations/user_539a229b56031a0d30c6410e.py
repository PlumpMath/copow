#
#
# This file was autogenerated by PythonOnWheels (copow version)
# But YOU CAN EDIT THIS FILE SAFELY
# It will not be overwritten by python_on_wheels
# unless you force it with the -f or --force option
# 
# 2014/06/12 23:58:51


import sys
import os

import #APPNAME.lib.powlib
from #APPNAME.lib.pow_objects import Migration
from #APPNAME.models.user import User

migration = Migration()

def up():
    """ up method will be executed when running do_migrate -d up"""
    user = User( schema  = { 
           "loginname"    :      { "type" : "string" }, 
           "firstname"    :      { "type" : "string" },
           "lastname"     :      { "type" : "string" },
           "email"        :      { "type" : "string" },
           "password"     :      { "type" : "string" }
           #"a_more_complex_one"    :       { "type" : "Text" , "index" : True, "default" : "something"}
      } 
    )

    # creates the tabke (collection) and the schema in migrations/schemas/
    migration.create_table(user)
    print("  Successfully migrated user -> mehtod: up()")
    
def down():
    """ down method will be executed when running do_migrate -d down"""
    # drops the table (collection) and removes the schema from migrations/schemas/
    user = User()
    migration.drop_table(user)
    print("  Successfully migrated user -> mehtod: down()")
    
