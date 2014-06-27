
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
import #APPNAME.config.settings as settings
from bson.objectid import ObjectId

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

    def initialize(self,    method_get=None, 
                            method_put=None,
                            method_post=None,
                            method_delete=None,
                            params=[]):
        """
            The paramter method is set to the value defined in the dict
            in routes->rest_routes.
            You can define your own parameters there.
            This is specifically used to route the request (call the following method in the controller)
            which is specified as the 3rd parameter in rest_routes.
            
        """
        self.method_get = method_get
        self.method_put = method_put
        self.method_post = method_post
        self.method_delete = method_delete
        self.params = params
        #print("self.method: ", self.method, "  ->  ", self.params)

    def get(self, *args, **kwargs):
        #print("self.method: ", method)
        if self.method_get == "echo":
            print("returning ECHO")
            return self.echo(*args,**kwargs)
        else:
            print("returning copow routing")
            super( #CONTROLLER_CAPITALIZED_NAMEController,self).get(*args,**kwargs)


    def echo(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/GET /#CONTROLLERNAME
            CRUD: READ
            show all #MODELNAME_PLURAL
        """
        result_formats = self.request.headers.get("Accept").split(",")
        return self.render("#CONTROLLER_LOWER_NAME_echo.html", request=self.request, 
            result=None, formats=result_formats)

    def show_html(self, id=None, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/GET /#CONTROLLERNAME/id
            CRUD: READ
            show one #MODELNAME
        """
        print("get *args: ", args)
        print("get kwargs: ", kwargs)
        print("show_html oid: ", id)
        result = self.model.find({"_id" : ObjectId(str(id)) })
        # if result.count()=1 self.model ist automatically set to result[0]
        return self.render("#CONTROLLER_LOWER_NAME_show.html", request=self.request, result=self.model)

    def show_json(self, oid, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/GET /#CONTROLLERNAME/id
            CRUD: READ
            show one post
        """
        print("get *args: ", args)
        print("get kwargs: ", kwargs)
        print("show_json oid: ", oid)
        result = self.model.find({"_id" : ObjectId(str(oid)) })
        #return result.to_json()
        #print("result: ", result)
        #print("result: ", result, " Num -> ", result.count())
        self.write(str(result[0].to_json()))

    def list_json(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/GET /#CONTROLLERNAME
            CRUD: READ
            show all posts
        """
        result = self.model.find_all()
        res_list = ""
        for mod in result:
            res_list += str(mod.to_json()) + ","
        # remove trailing comma before sending.
        self.write( res_list[:-1] )

    def list_html(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/GET /#CONTROLLERNAME
            CRUD: READ
            show all #MODELNAME_PLURAL
        """
        result = self.model.find_all()
        return self.render("#CONTROLLER_LOWER_NAME_list.html", request=self.request, result=result)

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

    def create_from_form(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/PUT /#CONTROLLERNAME 
            CRUD: CREATE 
            but eats the HTML Form input, not the json
            returns the form to create a new post
        """
        return self.render("#CONTROLLER_LOWER_NAME_create.html", request=self.request)
    
    def update(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/POST /#CONTROLLERNAME 
            CRUD: UPDATE 
            update really updates the data in the db
            data must be in json format
        """
        return self.render("#CONTROLLER_LOWER_NAME_update.html", request=self.request)        

    def update_form(self, id=None, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/POST /#CONTROLLERNAME 
            CRUD: UPDATE 
            returns the form to update a new #MODELNAME
        """
        print("get *args: ", args)
        print("get kwargs: ", kwargs)
        print("update_form oid: ", id)
        result = self.model.find({"_id" : ObjectId(str(id)) })
        # if result.count()=1 self.model ist automatically set to result[0]
        return self.render("#CONTROLLER_LOWER_NAME_update_form.html", 
                request=self.request, result=self.model, types=settings.schema_rypes
        )        

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

    


