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
from  #APPNAME.models.user import User

class LoginController(BaseController):
    
    def __init__(self, *args, **kwargs):
        self.model = User()
        super(LoginController,self).__init__(*args,**kwargs)

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
        
    #
    # called on get request (text/html)
    #
    def show_html(self, *args, **kwargs):
        #
        # below you can find some sample code 
        #
        self.render('login.html', result=self.model, request=self.request)
    

    #
    # called on post requests application/json
    #
    def check_login_json(self, *args, **kwargs):
        print("LoginController: check_login_json!")
        data = self.get_request_body_json_data(self.request)
        print("    --> data: ", data)
        loginname = data.get("loginname", None)
        password = data.get("password", None)
        print("loginname:", loginname)
        print("password:", password)
        if self.set_current_user(loginname, password):
            self.set_status(200)
            #self.redirect("/", loginname=loginname)
            self.write( json.dumps({ "data" : "/"}))
            self.finish()
        else:
            self.set_status(500)
            self.write( json.dumps({ "data" : "/login"}))
            self.finish()

    #
    # called on post requests application/x-www-form-urlencoded
    #
    def check_login_html(self, *args, **kwargs):
        print("this is login controller POST:")
        loginname = self.get_argument("loginname",None)
        password = self.get_argument("password", None)
        print("loginname:", loginname)
        print("password:", password)
        return self.react(loginname, password)


    def react(self, loginname, password):
        if loginname and password:
            #
            # check login
            # 
            if self.set_current_user(loginname, password):
                self.set_status(200)
                #self.redirect("/", loginname=loginname)
                self.render("welcome.html", argslist=self.path_args, kwargslist=self.path_kwargs, 
                    request=self.request, loginname=loginname)
            else:
                self.set_status(500)
                self.redirect("/login")
        else:
            self.set_status(500)
            self.redirect("/login")
        #self.set_secure_cookie("username", self.get_argument("username"))
        #self.redirect("/")



