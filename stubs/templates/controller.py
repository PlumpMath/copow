
#
# Controller: #CONTROLLERNAME
#
# generated: #DATE
# by PythonOnWheels (copow version)
#
# You can edit this file safely. It will only be
# overwritten if you specify it with the -f or --force option.
# 
import os
import os.path
import json

from #APPNAME.lib.db_conn import DBConn
#from #APPNAME.migrations.schemas.#MODEL_SCHEMA import #MODELNAME as schema
from #APPNAME.migrations.schemas import #MODEL_SCHEMA_schema as schema_module
import #APPNAME.migrations.schemas.#MODEL_SCHEMA_schema
from #APPNAME.lib import powlib

def #CONTROLLERNAME_list():
		""" respresents the folowing REST/CRUD Terminology:
			REST: HTTP/GET /#CONTROLLERNAME
			CRUD: READ
			show all #MODELNAMEs
		"""
		pass

def #CONTROLLERNAME_show():
		""" respresents the folowing REST/CRUD Terminology:
			REST: HTTP/GET /#CONTROLLERNAME/id
			CRUD: READ
			show one #MODELNAME
		"""
		pass

def #CONTROLLERNAME_create():
		""" respresents the folowing REST/CRUD Terminology:
			REST: HTTP/PUT /#CONTROLLERNAME 
			CRUD: CREATE 
			create really writes the new dataset #MODELNAME to DB
		"""
		pass		

def #CONTROLLERNAME_create_form():
		""" respresents the folowing REST/CRUD Terminology:
			REST: HTTP/PUT /#CONTROLLERNAME 
			CRUD: CREATE 
			returns the form to create a new #MODELNAME
		"""
		pass		

def #CONTROLLERNAME_update():
		""" respresents the folowing REST/CRUD Terminology:
			REST: HTTP/POST /#CONTROLLERNAME 
			CRUD: UPDATE 
			update really updates the data in the db
		"""
		pass		

def #CONTROLLERNAME_update_form():
		""" respresents the folowing REST/CRUD Terminology:
			REST: HTTP/POST /#CONTROLLERNAME 
			CRUD: UPDATE 
			returns the form to update a new #MODELNAME
		"""
		pass		

def #CONTROLLERNAME_delete_all():
		""" respresents the folowing REST/CRUD Terminology:
			REST: HTTP/DELETE /#CONTROLLERNAME
			CRUD: DELETE
			delete one #MODELNAME
		"""
		pass

def #CONTROLLERNAME_delete():
		""" respresents the folowing REST/CRUD Terminology:
			REST: HTTP/DELETE /#CONTROLLERNAME/id
			CRUD: DELETE
			delete all #MODELNAMEs
		"""
		pass