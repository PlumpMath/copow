#
#
# schema for the app model
# as an example there are already some attributes filled in.
# Generated: 2013/07/06 22:29:03
# 

app = {
	"name"              :      { "type" : "Text", "default" : "#APPNAME" },   
   	"path"              :      { "type" : "Text" },
   	"lastversion"       :      { "type" : "int" },
   	"currentversion"    :      { "type" : "int" },
   	"maxversion"        :      { "type" : "int" },

    "created"           :      { "type" : "date" },
    "last_updated"      :      { "type" : "date" },
    "_id"               :      { "type" : "id"  } 
}


app_relations = {
	#"comments" : "has_many"

}