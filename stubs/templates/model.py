#
#
# Model #MODELCLASS
# automatically created: #DATE by copow
# 
#

from copow.lib.db_conn import DBConn
from #APPNAME.migrations.schemas.#MODEL_SCHEMA_schema import #MODEL_SCHEMA as schema
from #APPNAME.models.basemodels.base#MODELNAME import Base#MODELCLASS

class #MODELCLASS(Base#MODELCLASS):
	
	def __init__(self, data=None, schema={}):
		super(#MODELCLASS, self).__init__(data)


