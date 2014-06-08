import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import os.path
import sys
import importlib

import #APPNAME.config.routes 
import #APPNAME.config.settings

#sys.path.append(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../config" )) 

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

copow_handlers = #APPNAME.config.routes.handlers
copow_settings = #APPNAME.config.settings.webserver

def init_controllers(app):
	"""
		automatically adds RESTful routes for eacg controller in controllers/
		which is named according to the convention: name_controller

		Automatically calls the right cotroller->CRUDMethod.
        According to this mapping table:
        **********
        * ACTION:
        **********
        in General:
        HTTP    Method      CRUD Action Description
        -----------------------------------------------
        POST    CREATE      Create a new resource
        GET     RETRIEVE    Retrieve a representation of a resource
        PUT     UPDATE      Update a resource
        DELETE  DELETE      Delete a resource

        PUT and DELETE must be handled with a POST request and an
        addiotional HTTP Parameter: REQUEST_TYPE
        set to PUT or DELETE accordingly.

        Meaning a call to domain:port/controller/([someting]+)
        Where something is usually an ID
        HTTP get        => will call controller.show(something)
        HTTP POST       => will call controller.create(something)
        HTTP PUT        => will call controller.edit(something)
        HTTP DELETE     => will call controller.delete(something)
        and a call to domain:port/controller/
        HTTP get        => will call controller.list()
        HTTP POST       => will call Nothing, yet.
        HTTP PUT        => will call controller.replace_all() [empty by default]
        HTTP DELETE     => will call controller.delete_all()

        ***********
        * FORMAT:
        ***********
        Also all reuests can have an Accept: HTTP header field which must be parsed by the
        controller itself.
        Example:    Accept:      text/json

        
	"""
	path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "controllers")
	print("-"*50)
	print("| Creating RESTful routes for these controllers: ")
	print("-"*50)
	handler_list = []
	exclude_list = [
		"base_controller", 
		"welcome_controller", 
		"error_controller", 
		"login_controller", 
		"logout_controller",
		"dispatch_controller"
	]
	for f in os.listdir(path):
		fname, fext = os.path.splitext(f)
		if not fname.startswith("__") and fname not in exclude_list:
			print("  -> ", fname)
			# create RESTful routes for each controller.
			# 1. load the controller
			# convention for the controller module name is: name_controller
			controller_name = fname.split("_")[0].capitalize()+"Controller"
			controller_short_name = fname.split("_")[0]
			import_module_str = "atest.controllers." + fname
			#print(import_module_str)
			con = importlib.import_module(import_module_str)
			#print(con)
			controller = getattr(con, controller_name)
			#print(controller)
			# 1st REST 
			onerest = r"/"+controller_short_name
			handler_list.append((onerest, controller))
			tworest = r"/"+controller_short_name+"/([0-9a-zA-Z]+)"
			handler_list.append((tworest, controller))
	#print(handler_list)
	app.add_handlers(".*$", handler_list)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=copow_handlers, **copow_settings)
	init_controllers(app)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

		