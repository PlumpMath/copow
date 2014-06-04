#
#
# PythonOnWheels Objects 
# khz
# 04/2013
#

import sys, datetime, os, getopt, shutil
import configparser
import string
import re
import time,datetime

from #APPNAME.lib import powlib
from #APPNAME.config import db
from #APPNAME.config import settings
from #APPNAME.lib import db_conn

class Migration(object):
    
    """
    Migrations functionality: (and implementation status)
     
        add_column                  =>      Done
        add_index                   =>      Done
        change_column               =>      Not Done
        change_table                =>      Not Done
        create_table                =>      Done
        drop_table                  =>      Done
        remove_column               =>      Done
        remove_index                =>      Done
        rename_column               =>      Not Done
    """

    def __init__(self):   
       self.collection = None
       self._db_conn = DBConn()
       self.db = self._db_conn.get_db()
    
    def add_column( self, model, name, attrs={}):
        model.load_schema()
        mdoel.add_column(name, attrs) 
        model.create_schema()

    def remove_column(self,name, filter={}):
        model.load_schema()
        mdoel.remove_column(name, filter) 
        model.create_schema()

    def remove_index(self,name):
        model.load_schema()
        model.remove_index(name)
        model.create_schema()
   
    def create_table(self, model):
        """ created a collection 
            (its not neccessary to do that explicitly 
            but increases clarity

            :type model:    a copow model
        """
        model.create_schema()
        model.create_table()
        return model

    def drop_table(self, model):
        """ drops a collection 
            :type model:    a copow model
        """
        return model.drop_table()

    def add_index(self, table, column="", **kwargs):
        """ adds an index to the given table and column.
            :type model:    a copow model
            :type column:   str

            example for the mongoDB collection operation:
                 coll.create_index("title", name="title_index_khz", unique=True)
        """
        # add the index to the db
        try:
            table.add_index(*args, **kwargs)
            #adapt the schema
            pass
        except Exception as e:
            raise e    
        
    
    def is_tree(cls, is_root=False):
        """ creates the neccessary attributes to represent this model in a tree structure.
            Tree handling model is: model tree structures with child references
            see: http://docs.mongodb.org/manual/tutorial/model-tree-structures-with-child-references/
            (I added a parent ref, as well)

            example:
            ---------
            Books
                |- Programming
                        |- Databases
                        |- Languages
            
            is modeled like:
            ----------------
            db.categories.insert( { _id: "Programming", children: [ "Databases", "Languages" ] } )
            db.categories.insert( { _id: "Books", children: [ "Programming" ] } )
        """
        
        # 0. check if model exists
        module = importlib.import_module("#APPNAME.models." + cls.modelname)
        schema = reload(schema_module)
        relations = schema.__dict__[cls.modelname+"_relations"]
        # 1. check if relation is not already existing
        try: 
            if relations[cls.modelname] == "tree":
                raise Exception( "POWError: model %s already is a tree relation " % (cls.modelname) )
                return
        except Exception as e:
            # nothing to be done if key is not present.
            pass

        # 2. add the tree to relations      
        print(" .. creating a tree relation")
        cls.relations[powlib.plural(cls.modelname)] = "tree"
        #3. add the according attributes to the class (cls)
        cls.schema["_id"] = { "type" : "string" }
        cls.schema["children"] = { "type" : "list" }
        # today only one parent is supported.
        cls.schema["parent"] = { "type" : "list" }
        
        cls.create_schema()
        
        return cls


   