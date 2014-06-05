#
#
# Model App
# automatically created: 2013/07/10 17:14:14 by copow
# 
#

from #APPNAME.lib.db_conn import DBConn
from #APPNAME.migrations.schemas.app_schema import app as schema
#from #APPNAME.models.basemodels.baseapp import BaseApp
from #APPNAME.models.basemodels.base import BaseModel
import #APPNAME.lib.powlib as powlib

class App(BaseModel):
	
    def __init__(self, data=None, schema={}):
        """ Basic instance setup"""
        self.collection_name = "apps"
        self.modelname = "app"
        self.modelname_plural = powlib.pluralize(self.modelname)
        self._db_conn = DBConn()
        self.db = self._db_conn.get_db()
        self.collection = self.db[self.collection_name]
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
            self.set_data(data)


