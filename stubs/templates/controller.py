
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

import tornado.web
import os
from atest.controllers.base_controller import BaseController

class #CONTROLLERNAMEController(BaseController):

     """    All copow Controllers are tornado.web.RequestHandlers
            RESTful routing is automatically added for all controllers.

            So e.g.:        GET  hostname:port/controller1
            REST semantic:  list all controller1 ressources
            calls           controller.list()     

            If you want to handle things before any methiod call, just 
            put it in the before() method.

            Access can be restricted by labeling the protected method
            with the @tornado.web.authenticated decorator.

            In addition to the standard you can choose between user or 
            role based authentication. See config/settings.base 
            authentication setting.
            
            You can also user twitter google or facebook authentication.
            Read the documentation for more details.

     """
    def prepare(self):
        """ called before any http get/pust method is called """
        pass

    def list(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/GET /#CONTROLLERNAME
                CRUD: READ
                show all #MODELNAMEs
            """
            pass

    def show(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/GET /#CONTROLLERNAME/id
                CRUD: READ
                show one #MODELNAME
            """
            pass

    def create(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/PUT /#CONTROLLERNAME 
                CRUD: CREATE 
                create really writes the new dataset #MODELNAME to DB
            """
            pass        

    def create_form(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/PUT /#CONTROLLERNAME 
                CRUD: CREATE 
                returns the form to create a new #MODELNAME
            """
            pass        

    def update(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/POST /#CONTROLLERNAME 
                CRUD: UPDATE 
                update really updates the data in the db
            """
            pass        

    def update_form(*args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/POST /#CONTROLLERNAME 
                CRUD: UPDATE 
                returns the form to update a new #MODELNAME
            """
            pass        

    def delete_all(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/DELETE /#CONTROLLERNAME
                CRUD: DELETE
                delete one #MODELNAME
            """
            pass

    def delete(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/DELETE /#CONTROLLERNAME/id
                CRUD: DELETE
                delete all #MODELNAMEs
            """
            pass