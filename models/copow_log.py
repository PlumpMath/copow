#
#
# Model Copow_log
# automatically created: 2014/07/24 00:30:32 by copow
# 
#

from #APPNAME.lib.db_conn import DBConn
from #APPNAME.migrations.schemas.copow_log_schema import copow_log as schema
#from #APPNAME.models.basemodels.basecopow_log import BaseCopow_log
from #APPNAME.models.basemodels.base import BaseModel
#import #APPNAME.lib.powlib
from #APPNAME.lib import powlib

from #APPNAME.ext.paginate import will_paginate

class Copow_log(BaseModel):
    db_conn = DBConn()
    db = db_conn.get_db()
    collection_name = "copow_logs"
    collection = db[collection_name]
    def __init__(self, *args, data={}, schema={}, **kwargs):
        #super(Copow_log, self).__init__(data)
        """ Basic instance setup"""
        #super(Copow_log,self).__init__(*args, **kwargs)
        #print("created a new Copow_log, id:", id(self))
        #self.collection_name = "copow_logs"
        self.modelname = "copow_log"
        self.modelname_plural = powlib.pluralize(self.modelname)
        #self._db_conn = DBConn()
        #self.db = self._db_conn.get_db()
        #self.collection = self.db[self.collection_name]
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
            self.set_values(data)

    # example for extension use
    # @will_paginate(per_page=10)
    # also look at the import above
    def find(self, *args, sort=False, **kwargs):
        return super(Copow_log,self).find(*args,**kwargs)
