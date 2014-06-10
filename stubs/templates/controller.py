
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
from #APPNAME.controllers.base_controller import BaseController
from  #APPNAME.models.#MODELNAME import #MODELCLASSNAME

class #CONTROLLER_CAPITALIZED_NAMEController(BaseController):

    """     All copow Controllers are tornado.web.RequestHandlers
            RESTful routing is automatically added for all controllers.

            So e.g.:        GET  hostname:port/controller1
            REST semantic:  list all controller1 ressources
            calls           controller.list()     

            If you want to handle things before any method call, just 
            put it in the before() method.

            Access can be restricted by labeling the protected method
            with the @tornado.web.authenticated decorator.

            In addition to the tornado standard you can choose between user 
            or role based authentication. See config/settings.base 
            authentication setting.

            You can also use twitter, google, facebook or other authentications
            like oauth, oauth2 ... 
            Read the documentation for more details.

    """

    def __init__(self, *args, **kwargs):
        self.model = #MODELCLASSNAME()
        super(#CONTROLLER_CAPITALIZED_NAMEController,self).__init__(*args,**kwargs)

    def prepare(self):
        """ called before any http get/pust method is called """
        pass

    def list(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/GET /#CONTROLLERNAME
                CRUD: READ
                show all #MODELNAME_PLURAL
            """
            result = self.model.find_all()
            return self.render("#CONTROLLER_LOWER_NAME_list.html", request=self.request, result=result)

    def show(self, *args, id=None, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/GET /#CONTROLLERNAME/id
                CRUD: READ
                show one #MODELNAME
            """
            result = self.model.find_one()
            return self.render("#CONTROLLER_LOWER_NAME_show.html", request=self.request, result=result)

    def create(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/PUT /#CONTROLLERNAME 
                CRUD: CREATE 
                create really writes the new dataset #MODELNAME to DB
            """
            return self.render("#CONTROLLER_LOWER_NAME_create.html", request=self.request)        

    def create_form(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/PUT /#CONTROLLERNAME 
                CRUD: CREATE 
                returns the form to create a new #MODELNAME
            """
            return self.render("#CONTROLLER_LOWER_NAME_create_form.html", request=self.request)        

    def update(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/POST /#CONTROLLERNAME 
                CRUD: UPDATE 
                update really updates the data in the db
                data must be in json format
            """
            return self.render("#CONTROLLER_LOWER_NAME_update.html", request=self.request)        

    def update_form(self, *args, id=None, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/POST /#CONTROLLERNAME 
                CRUD: UPDATE 
                returns the form to update a new #MODELNAME
            """
            return self.render("#CONTROLLER_LOWER_NAME_update_form.html", request=self.request)        

    def update_all(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/PUT /#CONTROLLERNAME
                CRUD: update_all
                update all #MODELNAME_PLURAL
            """
            self.set_status(501)
            self.render("error.html")


    def delete_all(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/DELETE /#CONTROLLERNAME
                CRUD: DELETE
                delete all #MODELNAME_PLURAL
            """
            return self.render("#CONTROLLER_LOWER_NAME_delete_all.html", request=self.request)

    def delete(self, *args, **kwargs):
            """ respresents the folowing REST/CRUD Terminology:
                REST: HTTP/DELETE /#CONTROLLERNAME/id
                CRUD: DELETE
                delete a #MODELNAME
            """
            return self.render("#CONTROLLER_LOWER_NAME_delete.html", request=self.request)

    


