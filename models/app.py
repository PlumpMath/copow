#
#
# Model App
# automatically created: 2013/07/10 17:14:14 by copow
# 
#

from #APPNAME.lib.db_conn import DBConn
from #APPNAME.migrations.schemas.app_schema import app as schema
from #APPNAME.models.basemodels.baseapp import BaseApp

class App(BaseApp):
	
	def __init__(self, data=None, schema={}):
		super(App, self).__init__(data)


