#
#
# Model App
# automatically created: 2014/07/24 00:30:23 by copow
# 
#

from #APPNAME.lib.db_conn import DBConn
from #APPNAME.migrations.schemas.app_schema import app as schema
#from #APPNAME.models.basemodels.baseapp import BaseApp
from #APPNAME.models.basemodels.base import BaseModel
#import #APPNAME.lib.powlib
from #APPNAME.lib import powlib

from #APPNAME.ext.paginate import will_paginate

class App(BaseModel):
    db_conn = DBConn()
    db = db_conn.get_db()
    collection_name = "apps"
    collection = db[collection_name]
    def __init__(self, *args, data={}, schema={}, **kwargs):
        #super(App, self).__init__(data)
        """ Basic instance setup"""
        #super(App,self).__init__(*args, **kwargs)
        #print("created a new App, id:", id(self))
        #self.collection_name = "apps"
        self.modelname = "app"
        self.modelname_plural = powlib.pluralize(self.modelname)
        #self._db_conn = DBConn()
        #self.db = self._db_conn.get_db()
        #self.collection = self.db[self.collection_name]
        #self.related_models = {}
        if schema:
            self.schema = schema
            if "app_relations" in schema.keys():
                self.relations = schema["app_relations"]
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
        return super(App,self).find(*args,**kwargs)
