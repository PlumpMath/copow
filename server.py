import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import os.path
import sys
import importlib

import #APPNAME.config.routes as routes
import #APPNAME.config.settings as settings

#sys.path.append(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../config" )) 

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

copow_handlers = routes.handlers
copow_settings = settings.webserver

def init_controllers(app):
	"""
		automatically generates RESTful routes for eacg controller in controllers/
		which is named according to the convention: name_controller

		Automatically calls the right cotroller->CRUDMethod.
        See controllers/base_controller.py for more details.

        
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
			controller = fname.split("_")[0]
			import_module_str = "atest.controllers." + fname
			#print(import_module_str)
			con = importlib.import_module(import_module_str)
			#print(con)
			controller_cls = getattr(con, controller_name)
			#print(controller)
			# 1st REST 
			#onerest = r"/"+controller
			#handler_list.append((onerest, controller_cls))
			#tworest = r"/"+controller+"/([0-9a-zA-Z]+)"
			#handler_list.append((tworest, controller_cls))
			#
			# edit
			#handler_list.append(("/"+controller_short_name+"/([0-9a-zA-Z]+)/(update)", controller))
			for route in routes.rest_routes.keys():
				# route[0] = the controller to handle the Request 
				# route[1] = an optional dict of paramenters passed to controller.initialize method.
				# see: tornado.RequestHandler.initialize
				abs_route = route.replace("#controller", controller)
				if routes.rest_routes[route][0] == "#controller_cls":
					if routes.rest_routes[route][1]:
						handler_list.append((abs_route, controller_cls, routes.rest_routes[route][1]))
					else:
						handler_list.append((abs_route, controller_cls))
				else:
					# a specific class is defined in the rest_routes
					# (for whatever reason ;) but anyway, load it.
					if routes.rest_routes[route][1]:
						handler_list.append((abs_route, routes.rest_routes[route],routes.rest_routes[route][1] ))
					else:
						handler_list.append((abs_route, routes.rest_routes[route]))

	app.add_handlers(".*$", handler_list)
	width=80
	print("-"*width)
	print("| RESTful routes semantic: (defined in routes.py")
	print("-"*width)
	print('{0:40} {1:8} {2:15} {3:15}'.format(
		"Route", "HTTP", "Method", "Parameters"
		)
	)
	print(""*width)
	for route in routes.rest_routes.keys():
		for method in ["GET", "POST", "PUT", "DELETE"]:
		 	print('{0:40} {1:8} {2:15} {3:15}'.format(
		 			route,
		 			method,
		 			routes.rest_routes[route][1]["method_"+method.lower()],
		 			routes.rest_routes[route][1]["params"]	
		 		)
		 	)
	print("-"*width)
	print("| The Standard REST methods input and output format is json.")
	print("-"*width)
if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=copow_handlers, **copow_settings)
	init_controllers(app)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

		