#
#
# Model User
# automatically created: 2014/06/05 14:32:45 by copow
# 
#

from atest.lib.db_conn import DBConn
from atest.migrations.schemas.user_schema import user as schema
#from atest.models.basemodels.baseuser import BaseUser
from atest.models.basemodels.base import BaseModel
#import atest.lib.powlib
from atest.lib import powlib

class User(BaseModel):
    
    def __init__(self, data=None, schema={}):
        #super(User, self).__init__(data)
        """ Basic instance setup"""
        self.collection_name = "users"
        self.modelname = "user"
        self.modelname_plural = powlib.pluralize(self.modelname)
        self._db_conn = DBConn()
        self.db = self._db_conn.get_db()
        self.collection = self.db[self.collection_name]
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
            self.set_data(data)


