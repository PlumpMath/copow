#
#
# schema for the app model
# as an example there are already some attributes filled in.
# Generated: 2013/07/06 22:29:03
# 

app = {
	"name"              :      { "type" : "string", "default" : "#APPNAME" },   
   	"path"              :      { "type" : "string" },
   	"lastversion"       :      { "type" : "integer" },
   	"currentversion"    :      { "type" : "integer" },
   	"maxversion"        :      { "type" : "integer" },
    "last_updated"      :      { "type" : "datetime" },
    "_id"               :      { "type" : "objectid"  } 
}


app_relations = {
	#"comments" : "has_many"

}