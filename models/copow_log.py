#
#
# Model Copow_log
# automatically created: 2014/06/05 14:28:25 by copow
# 
#

from atest.lib.db_conn import DBConn
from atest.migrations.schemas.copow_log_schema import copow_log as schema
#from atest.models.basemodels.basecopow_log import BaseCopow_log
from atest.models.basemodels.base import BaseModel
#import atest.lib.powlib
from atest.lib import powlib

class Copow_log(BaseModel):
    
    def __init__(self, data=None, schema={}):
        #super(Copow_log, self).__init__(data)
        """ Basic instance setup"""
        self.collection_name = "copow_logs"
        self.modelname = "copow_log"
        self.modelname_plural = powlib.pluralize(self.modelname)
        self._db_conn = DBConn()
        self.db = self._db_conn.get_db()
        self.collection = self.db[self.collection_name]
        #self.related_models = {}
        if schema:
            self.schema = schema
            if "copow_log_relations" in schema.keys():
                self.relations = schema["copow_log_relations"]
            else:
                self.relations = {}
        else:
            self.load_schema()
        self.setup_properties()
        #print self.schema
        #print dir(self)
        if data:
            self.set_data(data)


