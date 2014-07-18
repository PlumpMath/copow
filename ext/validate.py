#
# copow standard validations
# created by khz (2014)
#
# you can use / set them in your schema directly 
#   "comment"        :      { "type" : "Text", "validate" : [validate.lenght(0,10)] }
# or via migrations.
#   model.add_validation( attribute, validation)
#
# The following methods will automatcally validate:
#   create, update, save
#
#
import #APPNAME.lib.powlib
import cerberus
from cerberus import Validator

class CopowValidator(Validator):
    
    # below is an example from the cerberus documentation showing
    # how to implement your own custom validator:

    #def _validate_isodd(self, isodd, field, value):
    #    if isodd and not bool(value & 1):
    #        self._error(field, "Must be an odd number"

	def _validate_type_text(self, field, value):
   		""" Enables validation for type:teyt schema attribute.
   			Is exactly handled as type string but results in a different uimodule.
   			#TODO: maybe cut off this type and make uimodules definable in the schema is the
   			#TODO: better solution.

	   		:param field: field name.
	   		:param value: field value."""
		return super(CopowValidator, self)._validate_type_string(self, field, value)

	def _validate_type_objectid(self, field, value):
	   """ Enables validation for `objectid` schema attribute.

	   :param field: field name.
	   :param value: field value.
	   """
	   if not re.match('[a-f0-9]{24}', value):
	       self._error(field, ERROR_BAD_TYPE % 'ObjectId')


	def _validate_type_binary(self, field, value):
	   """ Enables validation for `binary` schema attribute.

	   :param field: field name.
	   :param value: field value.
	   """
	   return

	def _validate_type_object(self, field, value):
	   """ Enables validation for `object` schema attribute.

	   :param field: field name.
	   :param value: field value.
	   """
	   return


	def validate_model(model):
    	return super(CopowValidator, self).validate(model.to_json(encoder="encode_raw"), model.schema)

