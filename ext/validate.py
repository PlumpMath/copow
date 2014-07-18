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


def validate(model):
    v = cerberus.Validator()
    return v.validate(model.schema, model.to_json(encoder="encode_raw"))

