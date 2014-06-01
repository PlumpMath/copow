#
# copow standard validations
# created by khz (2014)
#
# you can use / set them in your schema directly 
# 	"comment"        :      { "type" : "Text", "validate" : [validate.lenght(0,10)] }
# or via migrations.
# 	model.add_validation( attribute, validation)
#
# The following methods will automatcally validate:
#   create, update, save
#
#
import #APPNAME.lib.powlib

def length(val, min, max):
	""" checks if a given value is in between the given from/to length 
	 	boundaries.
	 """
	 if len(val) < min and len(val) > max:
	 	return True
	 else:
	 	return False


