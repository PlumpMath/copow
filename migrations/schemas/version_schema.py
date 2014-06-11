#
#
# schema for the version model
# as an example there are already some attributes filled in.
# Generated: 2013/07/06 22:16:03
# 

version = {
	"short_name"    :    { "type"    : "Text" },   
    "long_name"     :    { "type"    : "Text" },
    "environment"   :    { "type"    : "Text" },
    "comment"       :    { "type"    : "Text" },
    "version"       :    { "type"    : "int"  },
    
    "created"       :    { "type"    : "date" },
    "last_updated"  :    { "type"    : "date" },
    "_id"               :      { "type" : "id"  } 
}


version_relations = {
	#"comments" : "has_many"

}