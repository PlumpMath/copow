#
#
# Stubs for the relation access (CRUD) conveniance methods
# 
# So if you say post.has_many("comments")
# You get the following conveniance methods:
# ------------------------------------------
# post.find_one_comment()
# post.find_all_comments()
# post.add_comment()
# post.delete_comment()
# post.update_comment()
#
# Which are defined here.
#
# All methods are named foo in here and will be renamed during 
# the concrete creation into fieldname_objectname.
# See base.py->generate_method()
#

rel_methods = {
    
    "find_one"  :
    """
    def foo(*args, comment = c, **kwargs):
        res = self.find_one( { "#PLURAL_RELMODEL" :  comment } )
        return res
    """
}


