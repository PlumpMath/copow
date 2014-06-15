
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

from  #APPNAME.models.#MODELNAME import #MODELCLASSNAME
from bson.objectid import ObjectId

class #CONTROLLER_CAPITALIZED_NAMEController(object):

    """     
        A Basic controller without any tornado 
    """

    def __init__(self, *args, **kwargs):
        self.model = #MODELCLASSNAME()


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
        return result

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
        return res_list[:-1] 


    def delete_all(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/DELETE /#CONTROLLERNAME
            CRUD: DELETE
            delete all #MODELNAME_PLURAL
        """
        pass

    def delete(self, *args, **kwargs):
        """ respresents the folowing REST/CRUD Terminology:
            REST: HTTP/DELETE /#CONTROLLERNAME/id
            CRUD: DELETE
            delete a #MODELNAME
        """
        pass

    


