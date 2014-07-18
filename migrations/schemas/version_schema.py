#
#
# schema for the version model
# as an example there are already some attributes filled in.
# Generated: 2013/07/06 22:16:03
# 

version = {
	"short_name"    :    { "type"    : "string" },   
    "long_name"     :    { "type"    : "string" },
    "environment"   :    { "type"    : "string" },
    "comment"       :    { "type"    : "string" },
    "version"       :    { "type"    : "integer"  },
    "last_updated"  :    { "type"    : "datetime" },
    "_id"           :    { "type" : "objectid"  } 
}


version_relations = {
	#"comments" : "has_many"

}