#
#
# Model User
# automatically created: 2014/07/24 00:30:37 by copow
# 
#

from #APPNAME.lib.db_conn import DBConn
from #APPNAME.migrations.schemas.user_schema import user as schema
#from #APPNAME.models.basemodels.baseuser import BaseUser
from #APPNAME.models.basemodels.base import BaseModel
#import #APPNAME.lib.powlib
from #APPNAME.lib import powlib

from #APPNAME.ext.paginate import will_paginate

class User(BaseModel):
    db_conn = DBConn()
    db = db_conn.get_db()
    collection_name = "users"
    collection = db[collection_name]
    def __init__(self, *args, data={}, schema={}, **kwargs):
        #super(User, self).__init__(data)
        """ Basic instance setup"""
        #super(User,self).__init__(*args, **kwargs)
        #print("created a new User, id:", id(self))
        #self.collection_name = "users"
        self.modelname = "user"
        self.modelname_plural = powlib.pluralize(self.modelname)
        #self._db_conn = DBConn()
        #self.db = self._db_conn.get_db()
        #self.collection = self.db[self.collection_name]
        #self.related_models = {}
        if schema:
            self.schema = schema
            if "user_relations" in schema.keys():
                self.relations = schema["user_relations"]
            else:
                self.relations = {}
        else:
            self.load_schema()
        self.setup_properties()
        #print self.schema
        #print dir(self)
        if data:
            self.set_values(data)

    # example for extension use
    # @will_paginate(per_page=10)
    # also look at the import above
    def find(self, *args, sort=False, **kwargs):
        return super(User,self).find(*args,**kwargs)
