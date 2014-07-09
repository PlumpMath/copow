
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
import datetime

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
        if result.count() == 1:
            print("Yes, there is exactly 1 result, good !")
            return self.render("#CONTROLLER_LOWER_NAME_show.html", request=self.request, result=result[0])
        else:
            self.set_status(501)
            self.render("error.html", message=" No such ObjectID " + str(id))

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
        if result.count() == 1:
            self.write(str(result[0].to_json()))
        else:
            self.write({ "error" : "No such ObjectId"} )

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
        return self.render("#CONTROLLER_LOWER_NAME_list.html", request=self.request, result_model=self.model, result=result)

    def create(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/PUT /#CONTROLLERNAME 
            CRUD: CREATE 
            create really writes the new dataset #MODELNAME to DB
        """
        return self.render("#CONTROLLER_LOWER_NAME_create.html", request=self.request)        

    def create_form_html(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/PUT /#CONTROLLERNAME 
            CRUD: CREATE 
            returns the form to create a new #MODELNAME
        """
        self.model = self.model.__class__()
        return self.render("#CONTROLLER_LOWER_NAME_create_form.html", request=self.request, result=self.model)        

    def create_json(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/PUT /#CONTROLLERNAME 
            CRUD: CREATE 
            but eats the HTML Form input, not the json
            returns the form to create a new post
        """
        print("create_json *args: ", args)
        print("create_json kwargs: ", kwargs)
        #print("update_json request: ", self.request)
        #print("request body: ", self.request.body)
        #
        # getting the data payload
        #
        data = json.loads(self.request.body.decode(settings.base["default_encoding"]))
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print("data: ", data)
        try:
            self.model.set_values(data)
            self.model.create()
            print("model is now: ", self.model)
            ret_data = dict( data = self.model.to_json())
            #print("returning: ", ret_data)
            self.set_status(200)
            self.set_header("Content-Type", "application/json")
            print("headers: ", self._headers)
            self.write(tornado.escape.json_encode(ret_data))
        except Exception as e:
            ret_data = dict( data = 'Uuups: ' + now + str(e))
            #print("returning: ", ret_data)
            self.set_status(400)
            self.set_header("Content-Type", "application/json")
            print("headers: ", self._headers)
            self.write(tornado.escape.json_encode(ret_data))
        finally:
            self.finish()  
        #return self.render("#CONTROLLER_LOWER_NAME_create.html", request=self.request)

    @tornado.web.asynchronous    
    def update_json(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/POST /#CONTROLLERNAME 
            CRUD: UPDATE 
            update really updates the data in the db
            data must be in json format
        """
        print("update_json *args: ", args)
        print("update_json kwargs: ", kwargs)
        #print("update_json request: ", self.request)
        #print("request body: ", self.request.body)
        #
        # getting the data payload
        #
        data = json.loads(self.request.body.decode(settings.base["default_encoding"]))
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print("data: ", data)
        try:
            self.model.set_values(data)
            self.model.update()
            print("model is now: ", self.model)
            ret_data = dict( data = self.model.to_json())
            #print("returning: ", ret_data)
            self.set_status(200)
            self.set_header("Content-Type", "application/json")
            print("headers: ", self._headers)
            self.write(tornado.escape.json_encode(ret_data))
        except Exception as e:
            ret_data = dict( data = 'Uuups: ' + now + str(e))
            #print("returning: ", ret_data)
            self.set_status(400)
            self.set_header("Content-Type", "application/json")
            print("headers: ", self._headers)
            self.write(tornado.escape.json_encode(ret_data))
        finally:
            self.finish()               

    def update_form_html(self, id=None, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/POST /#CONTROLLERNAME 
            CRUD: UPDATE 
            returns the form to update a new #MODELNAME
        """
        print("get *args: ", args)
        print("get kwargs: ", kwargs)
        print("update_form oid: ", str(id))
        result = self.model.find({"_id" : ObjectId(str(id)) })
        # if result.count()=1 self.model ist automatically set to result[0]
        if result.count() == 1:
            return self.render("#CONTROLLER_LOWER_NAME_update_form.html", request=self.request, 
                result=result[0], types=settings.schema_types
            )
        else:
            self.set_status(501)
            self.render("error.html", message=" No such ObjectID " + str(id))


    def update_all(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/PUT /#CONTROLLERNAME
            CRUD: update_all
            update all #MODELNAME_PLURAL
        """
        self.set_status(501)
        self.render("error.html", message="Method not implemented, yet!")

    @tornado.web.asynchronous 
    def delete(self, id=None, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/DELETE /#CONTROLLERNAME/id
            CRUD: DELETE
            delete a post
        """
        print("delete id: ", str(id))
        if id:
            res = None
            res = self.model.find_by("_id", ObjectId(id))
            print("delete: res: ", res)
            if res != None:
                print("now its getting closer ...")
                res.delete()
                ret_data = dict( data = str(id))
                self.write(tornado.escape.json_encode(ret_data))
                self.finish()     
            else:
                print("No res !!")
                self.set_status(501)
                self.render("error.html", message=" No such ObjectID ", result=self.model)
        #return self.render("post_delete.html", request=self.request)


    def delete_all(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/DELETE /#CONTROLLERNAME
            CRUD: DELETE
            delete all #MODELNAME_PLURAL
        """
        #return self.render("#CONTROLLER_LOWER_NAME_delete_all.html", request=self.request)
        self.set_status(501)
        self.render("error.html", message="Method not implemented, yet!")
        

    


