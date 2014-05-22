#
#
# Model Version
# automatically created: 2013/07/06 22:16:03 by copow
# 
#

from #APPNAME.lib.db_conn import DBConn
from #APPNAME.migrations.schemas.version_schema import version as schema
from #APPNAME.models.basemodels.base import BaseModel

class Version(BaseModel):
    
    def __init__(self, data=None, schema={}):
        #super(Version, self).__init__(data)
        """ Basic instance setup"""
        self.collection_name = "versions"
        self.modelname = "version"
        self._db_conn = DBConn()
        self.db = self._db_conn.get_db()
        self.collection = self.db[self.collection_name]
        #self.related_models = {}
        if schema:
            self.schema = schema
            if schema.has_key("version_relations"):
                self.relations = schema["version_relations"]
            else:
                self.relations = {}
        else:
            self.load_schema()
        self.setup_properties()
        #print self.schema
        #print dir(self)
        if data:
            self.set_data(data)


