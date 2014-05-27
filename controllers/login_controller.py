#
# copow default LoginController
# 
import tornado.web
import os

from #APPNAME.controllers.base_controller import BaseController

class LoginController(BaseController):
    def get(self):
        self.render('login.html')
    
    def post(self):
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect("/")