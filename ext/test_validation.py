#
# CopowValidator test
#

from #APPNAME.ext.validate import CopowValidator
from #APPNAME.models.post import Post
width=30
v = CopowValidator()
p=Post()
print("-"*width)
print("  schema is:")
print("-"*width)
p.print_schema()
print("-"*width)
print("  instance is:")
print("-"*width)
p.find_one()
print(p)
r=v.validate_model(p)
print("-"*width)
print("  is valid: ", r)
print("  errors: ", v.errors)
print("-"*width)

