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
# and a call to domain:port/controller/
#   Where something is usually an ID
#   HTTP get        => will call controller.list()
#   HTTP POST       => will call Nothing, yet.
#   HTTP PUT        => will call controller.replace_all() [empty by degfault]
#   HTTP DELETE     => will call controller.delete_all()
#
# 

import #APPNAME.controllers.hello
# Add your routes below.
# Detaisl about formatting routes: 
handlers = [
        (r"/hello", #APPNAME.controllers.hello.HelloController) 
        ]