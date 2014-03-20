#
#
# Model Version
# automatically created: 2013/07/06 22:16:03 by copow
# 
#

from copow.lib.db_conn import DBConn
from copow.migrations.schemas.version_schema import version as schema
from copow.models.basemodels.baseversion import BaseVersion

class Version(BaseVersion):
	
	def __init__(self, data=None, schema={}):
		super(Version, self).__init__(data)


