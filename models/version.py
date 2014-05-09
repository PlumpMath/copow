#
#
# Model Version
# automatically created: 2013/07/06 22:16:03 by copow
# 
#

from #APPNAME.lib.db_conn import DBConn
from #APPNAME.migrations.schemas.version_schema import version as schema
from #APPNAME.models.basemodels.baseversion import BaseVersion

class Version(BaseVersion):
	
	def __init__(self, data=None, schema={}):
		super(Version, self).__init__(data)


