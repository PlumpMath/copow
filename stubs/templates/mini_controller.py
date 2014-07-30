#
# copow default LoginController
# 
import tornado.web
import os
import json
from bson.objectid import ObjectId
import datetime
import #APPNAME.config.settings as settings
from #APPNAME.controllers.base_controller import BaseController
#from  #APPNAME.models.#MODELNAME import #MODELCLASSNAME

class #CONTROLLER_CAPITALIZED_NAMEController(BaseController):
    
    def __init__(self, *args, **kwargs):
        #self.model = #MODELCLASSNAME()
        super(#CONTROLLER_CAPITALIZED_NAMEController,self).__init__(*args,**kwargs)

    def prepare(self):
        """ called before any http get/pust method is called """
        pass

    def initialize(self, *args,**kwargs):
        """
            The paramter method is set to the value defined in the dict
            in routes->rest_routes.
            You can define your own parameters there.
            This is specifically used to route the request (call the following method in the controller)
            which is specified as the 3rd parameter in rest_routes.
            
        """
        print("args: ", args, "  kwargs: ", kwargs)
        print("i am in initialize")
        print(self.request)
        print(self.request.body)
        

    def get(self, *args, **kwargs):
        #
        # below you can find some sample code 
        #
        self.render('login.html', result=self.model, request=self.request)
    

    def post(self, *args, **kwargs):
        #
        # below you can find some sample code 
        # data must be json
        # 
        print(self.request)
        data = get_request_body_json_data(self.request)    
        self.set_status(200)
        self.write(json.dumps({ "data" : "Succesfully returned" }))
        #self.set_secure_cookie("username", self.get_argument("username"))
        #self.redirect("/")