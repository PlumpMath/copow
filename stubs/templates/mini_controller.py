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
        #
        # below you can find some sample code 
        #
        print(self.request)
        #self.render('apage.html', result=self.model, request=self.request)
    

    def post(self, *args, **kwargs):
        #
        # below you can find some sample code 
        # data must be json
        # 
        print(self.request)
        



