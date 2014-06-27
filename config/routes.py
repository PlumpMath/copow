#
#
# copow routings
# 
# Standard is RESTful:
#
# meaning a call to domain:port/controller/([someting]+)
#   Where something is usually an ID
#   HTTP get        => will call controller.show(something)
#   HTTP POST       => will call controller.create(something)
#   HTTP PUT        => will call controller.edit(something)
#   HTTP DELETE     => will call controller.delete(something)
#   and a call to domain:port/controller/
#   Where something is usually an ID
#   HTTP get        => will call controller.list()
#   HTTP POST       => will call Nothing, yet.
#   HTTP PUT        => will call controller.replace_all() [empty by degfault]
#   HTTP DELETE     => will call controller.delete_all()
#
# 

import #APPNAME.controllers.welcome_controller
import #APPNAME.controllers.login_controller
import #APPNAME.controllers.logout_controller
import #APPNAME.controllers.error_controller


# default RESTful routes 
#  #controller will be replaced by the controllername for any controller in ./controllers
#  #controller_cls will be replaced by the actual class like:
#    .#APPNAME.controllers.controllername_python.ClassName

rest_routes = {
        r"/#controller"                                :     ("#controller_cls", dict(  method="list", 
                                                                                        params=[])),
        r"/#controller/echo"                           :     ("#controller_cls", dict(  method="echo", 
                                                                                        params=[])),
        r"/#controller/create"                         :     ("#controller_cls", dict(  method="create_form", 
                                                                                        params=[])),
        r"/#controller/([0-9a-zA-Z]+)"                 :     ("#controller_cls", dict(  method="show", 
                                                                                        params=["id"])),
        r"/#controller/([0-9a-zA-Z]+)/update"          :     ("#controller_cls", dict(  method="update_form", 
                                                                                        params=["id"]))
}

# Add your routes below.
# Details about formatting routes can be found in the documentation

# www.pythononwheels.org/copow/documentation/routes
handlers = [
        (r'/welcome', #APPNAME.controllers.welcome_controller.WelcomeController),
        (r'/features', #APPNAME.controllers.welcome_controller.WelcomeController),
        (r'/next-steps', #APPNAME.controllers.welcome_controller.WelcomeController),
        (r'/twitter', #APPNAME.controllers.welcome_controller.WelcomeController),
        (r'/login', #APPNAME.controllers.login_controller.LoginController),
        (r'/logout', #APPNAME.controllers.logout_controller.LogoutController),
        #
        # REST Handling via Dispatcher
        #
        #(r'/(w+)/', #APPNAME.controllers.dispatch_controller.DispatchController),
        #(r'/(w+)/([0-9]+)', #APPNAME.controllers.dispatch_controller.DispatchController),
        #
        # Anything else => ERROR
        #
        #(r'.*', #APPNAME.controllers.error_controller.ErrorController)
        ]