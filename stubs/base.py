#
#
# Model version 
# automatically created: 2013/07/06 22:16:03 by copow
# 
#
import string
import types
import importlib
import os
import os.path
import json
import imp
import pymongo
import pprint 

from #APPNAME.lib.db_conn import DBConn
from #APPNAME.lib import powlib
from #APPNAME.lib.powlib import _log
import #APPNAME.config.settings as settings

newline = powlib.newline
tab = powlib.tab

class BaseModel(object):
    
    #def __init__(self, data=None, schema=None):
    def __setitem__(self, key, value):    
        """ sets the objects attributes according to the search/find result
            Uses the as_class parameter of the find methods. 
            See http://dirolf.com/2010/06/17/pymongo-1.7-released.html
        """
        #print("in __setitem__")
        if key in self.schema.keys() or key == "_id":
            #print("object: ", self ," in __setitem__ for: ", key, " --> ", str(value))
            setattr(self, key, value) 
        else:
            raise Exception( "POWError: model %s has no column %s" % (self.modelname, key) )
        return 

    def set_data(self, data={}):
        """ set the data for this model from given dictionary data"""
        for key in list(data.keys()):
            if key in self.schema:
                #self.__dict__[key] = data[key]
                setattr(self,key, data[key])
            else:
                raise Exception("unknown attribute: %s for model: %s ") (key, self.modelname)   


    def setup_relations(self):
        self.related_models = {}
        for rel_model in list(self.relations.keys()):
            # check relation type
            #print("  -> setting up relation for: %s " % (rel_model))
            
            if self.relations[rel_model] == "has_many":
                rel_model = powlib.singularize(rel_model)
                module = importlib.import_module("#APPNAME.models." + rel_model )
                #print(module)
                #print(dir(module))
                rel_model_instance = getattr(module, str.capitalize(rel_model) )()
                self.related_models[rel_model] = rel_model_instance
                self.generate_accessor_methods(rel_model_instance)
            
            elif self.relations[rel_model] == "belongs_to":
                pass
            else:
                raise Exception("unknown relation: %s ") %(rel_model)

    def load_schema(self):
        try:
            """Tries to find the according schema in migrations/schemas/Version.py 
            imports the schema and sets the according properties in this class/instance"""
            schema_module = __import__("#APPNAME"+".migrations.schemas." + self.modelname + "_schema", 
                globals(), locals(), [self.modelname], 0)

            schema = imp.reload(schema_module)
        
            self.schema = schema_module.__dict__[self.modelname]
            self.relations = schema_module.__dict__[self.modelname + "_relations"]
        except Exception as e:
            print("Unexpected Error:", e, e.args)
            raise e

    def setup_properties(self):
        """ sets the accessor methods for the schema """
        # add the property and initialize it according to the type
        for column, attrs in list(self.schema.items()):
            #print("column : %s" % (column))
            #type = string.lower(attrs["type"])
            att_type = attrs["type"].lower()
            if att_type in settings.schema_types:
                #print "setting up property for: %s" % (column)
                #setting the according attribute and the default value, if any.
                setattr(self, column, settings.schema_types[att_type][0])
                setattr(self, column+"_type", att_type)
                setattr(self, column+"_uimodule", settings.schema_types[att_type][1])
            else:
                raise Exception("no or unknown type given in schema: version_schema.py. Type was: ", att_type)
            if "index" in attrs:
                att_index = attrs["index"]
                setattr(self, column+"_has_index", True)
            else:
                setattr(self, column+"_has_index", False)
            if "default" in attrs:
                att_default = attrs["default"]
                setattr(self, column+"_dafault", att_default)
            if "validation" in attrs:
                # this is just a quick indication if there is any validation or
                # not. If so, the real validation is loaded. So quick test, long loading 
                # only if True. 
                att_validation = attrs["validation"]
                setattr(self, column+"_has_validation", True)
            else:
                setattr(self, column+"_has_validation", False)
        
        self.setup_relations()

    
    def is_valid(self):
        for column in self.schema.keys():
            ## TODO
            if getattr(self,column + "_has_validation"):
                # validate this column
                pass
            else:
                # do  nothing
                pass
            return True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        #ostr = ""
        #adict = self.to_json()
        #for key in adict:
        #    ostr += key + " -> " + str(adict[key]) + os.linesep 
        #return ostr
        pp = pprint.PrettyPrinter(indent=4)
        str(pp.pprint(self.to_json()))
        return ""
        

    def get(self, attribute_name=None, as_str=True):
        """ returns the model attribute with the specified attribute_name"""
        if attribute_name:
            if as_str:
                return str(getattr(self,attribute_name))
            else:
                return getattr(self,attribute_name)

    def generate_method(self, method_name, method_str, replace = []):
        """ generates a method for this object based on the 
        given method_name and  method_str
        param: replace is a list of 2-tuples [(old_str, replace_str),..] """    
        for elem in replace:
            method_str = method_str.replace(elem[0], elem[1])
        print("method_str: ", method_str)
        exec(method_str,globals())
        self.__dict__[method_name] = types.MethodType(foo,self)
        #setattr(self, method_name, foo)

    def generate_accessor_methods(self, rel_model):
        """generates the convenient getAttribute() and setAttribute Methods
        and sets them as accessors for this models Attributes """
        #print(rel_model)
        #print(type(rel_model))
        #print(dir(rel_model))

        rel_model_name = rel_model.modelname
        # prepare the tmp attribute for the full models of a relation.
        setattr(self, powlib.pluralize(rel_model_name) +"_full", [])
        mstr = ""
        #add rel model
        mstr = ""
        method_name = "add_"+ rel_model_name
        tmp_meth_name = "foo"
        mstr +=     "def foo(self, model):" + newline
        mstr += tab + "self." + powlib.pluralize(rel_model_name) +".append(model._id) "+ os.linesep
        mstr += tab + "self." + powlib.pluralize(rel_model_name) +"_full.append(model) "+ os.linesep

        mstr += tab + "setattr(rel_model_instance, 'self.modelname' + '_id', self._id) "+ os.linesep
        mstr += tab + "return self." + powlib.pluralize(rel_model_name) + os.linesep
        exec(mstr,globals())
        self.__dict__[method_name] = types.MethodType(foo,self)
        #setattr(self, method_name, foo)
        
        
        # get a rel model
        mstr = ""
        method_name = "get_"+ powlib.pluralize(rel_model_name)

        tmp_meth_name = "foo"
        mstr +=     "def foo(self):" + newline
        mstr += tab + "return self." + powlib.pluralize(rel_model_name) +"_full" + os.linesep
        #print mstr
        exec(mstr,globals())
        self.__dict__[method_name] = types.MethodType(foo,self)
        #setattr(self, method_name, foo)
        

    def find_by(self, field, value):
        """ find model by attribute. Sets self to the model found.
            Uses find_one internally. """
        res = self.collection.find_one({ field : value })
        for column in res:
            if column in self.schema.keys():
                setattr(self, column, res[column])
            else:
                raise Exception( "POWError: model %s has no column %s" % (self.modelname, column) )
        return self

    def find_all(self, *args, **kwargs):
        """ Find all matching models. Returns an iterable.
            Uses model.find internally. More docu can be found there
        """
        return self.find(*args,**kwargs)

    
    def find(self, *args, sort=False, **kwargs):
        """ Find all matching models. Returns an iterable.
            sorting can be done by giving for exmaple: 
            sort=[("field", pymongo.ASCENDING), ("field2", pymongoDESCENDING),..]
            returns: a pymongo.cursor.Cursor
        """
        #print("args: ", *args)
        #print("kwargs: ", **kwargs)
        if sort:
            cursor = self.collection.find(*args, as_class=self.__class__, **kwargs).sort(sort)
        else:
            cursor = self.collection.find(*args, as_class=self.__class__, **kwargs)
        if cursor.__class__ == pymongo.cursor.Cursor:
            if cursor.count() == 1:
                # if it is only one result in the cursor, return the cursor but also 
                # set this (self) object's values as the result.
                self.set_values(cursor[0].to_json())
        return cursor


    def find_one(self, *args, **kwargs):
        """ Updates this(self) object directly.
            returns self (NOT a dict)
        """
        #ret = self.collection.find_one(*args, as_class=self.__class__, **kwargs)
        ret = self.collection.find_one(*args, **kwargs)
        if ret:
            self.set_values(ret)
        return self
    
    def set_values(self, dictionary):
        for elem in dictionary:
            self.__setitem__(elem, dictionary[elem])
        return

    def clear(self):
        """
            erase the instance's values
        """
        for elem in self.schema.keys():
            # get the according default type for the attribute 
            # See: settings.schema_types
            default_value = settings.schema_types[self.schema[elem]["type"].lower()]
            setattr(self, elem, default_value)
        print("erased values: ", self.to_json())
        return
    
    def save(self, safe=True):
        """ Saves the object. Results in insert if object wasnt in the db before,
            results in update otherwise"""
        d = self.to_json()
        d["last_updated"] = powlib.get_time()
        self._id = self.collection.save(d,  safe=safe)
        print("saved: ", self.modelname, " id: ",str(self._id))
        #self._id = self.insert(safe=safe)
        return self._id

    def insert(self, safe=True):
        """ Uses pymongo insert directly"""
        d = self.to_json()
        d["last_updated"] = powlib.get_time()
        #d["created"] = powlib.get_time()
        del d["_id"]
        self._id = self.collection.insert(d, safe=safe)
        print("inserted: ", self.modelname, " id: ", str(self._id))
        return self._id
        
    def create(self):
        """ Alias for insert()"""
        return self.insert()

    def update(self, *args, safe=True, multi=False, **kwargs):
        """  Pure: pymongo update. Can update any document in the collection (not only self)
            Syntax: db.test.update({"x": "y"}, {"$set": {"a": "c"}}) """
        #ret = self.collection.update(*args, **kwargs)
        ret = self.collection.update({"_id": self._id}, self.to_json(), safe=safe, multi=False )
        print("updated: ", self.modelname, " id: ", str(self._id))
        return ret
    
    def from_json(self, json_data):
        """ makes an self instance from json """
        return self.set_values(json_data)


    def to_json(self):
        """ returns a json representation of the schema"""
        d = {}
        for column in list(self.schema.keys()):
            d[column] = getattr(self, column)
        return d
    
    def log(self, type, message, *args):
        _log(type, '%s - - [%s] %s\n' % (self.modelname,
                                         "NOW ;)",
                                         message % args))

    def reload_relations(self):
        """
            (re)load the models relations from the schema (as a module)
            migrations/schemas/modelname_schema.py
        """
        schema_module = __import__("#APPNAME"+".migrations.schemas." + self.modelname + "_schema", 
                globals(), locals(), [self.modelname], 0)        
        schema = imp.reload(schema_module)
        #schema = reload(schema_module)
        self.relations = schema_module.__dict__[self.modelname + "_relations"]
        return self.relations

    def has_many(self, rel_model, one_to_one=False ):
        """ creates an (currently embedded) one:many relation between this (self) and model.
            see doc in source below.
        """

        if type(rel_model) == str:
            rel_modelname = powlib.singularize(rel_model)
        else:
            rel_modelname = rel_model.modelname
        print(" rel_modelname: ", rel_modelname)
        # 0. check if relation is not already existing
        if powlib.plural(rel_modelname) in self.relations:
            raise Exception( "POWError: model %s already has a relation to %s " % (self.modelname, rel_modelname) )
            return
        # 1. check if model exists
        try:
            module = importlib.import_module("#APPNAME.models." + rel_modelname )
            #print(module)
            #print(dir(module))
            rel_model_instance = getattr(module, str.capitalize(rel_modelname) )()
            #print(rel_model_instance)
        except Exception as e:
            raise e    
        
        rel = self.reload_relations()
        
        # 2. add list of related model to relations
        print(" creating the according object attributes:")
        print("-"*50)
        print("  ++ attribute for a 1:n relation : ", self.modelname + "." + rel_modelname + " type: []")
        self.relations[powlib.plural(rel_modelname)] = "has_many"
        self.schema[powlib.plural(rel_modelname)] = { "type" : "list" }
        try:
            self.create_schema()
        except Exception as e:
            raise e

        print("  ++ attribute for a 1:1 relation : ", rel_modelname + "." + self.modelname + "_id type: ObjectId")
        rel_model_instance.relations[self.modelname] ="belongs_to"
        rel_model_instance.schema[self.modelname+"_id"] = { "type" : "ObjectId" }
        try:
            rel_model_instance.create_schema()
        except Exception as e:
            raise e
        self.generate_accessor_methods(rel_model_instance)

    def has_one(self, model, embedd=True):
        """ creates an (currently embedded) one:one relation between this (self) and model."""
        return self.has_many(model, embedd, one_to_one=True)
            
    def remove_relation(self, rel_model):
        """ tries to find the given relation by its name and deltes the relation entry and the
            instance and class attribute, as well."""
        print("in remove_relation: ", self)
        if type(rel_model) == str:
            rel_modelname = rel_model
        else:
            rel_modelname = rel_model.modelname
        try:
            # 0. check if model exists
            rel = self.reload_relations()
            # 1. check if relation is existing
            if powlib.plural(rel_modelname) in self.relations or rel_modelname in self.relations:
                pass
            else:    
                raise Exception( "POWError: model %s already norelation to %s " % (self.modelname, rel_modelname) )
            # 2. remove the relation 
            # has_many
            if powlib.plural(rel_modelname) in self.relations.keys():
                print("removing relation (has_many): ", self.modelname, " -> ", rel_modelname)
                del self.relations[powlib.plural(rel_modelname)]
                del self.schema[powlib.plural(rel_modelname)]
                # delete the belongs to in the rel_model as well
                try:
                    module = importlib.import_module("#APPNAME.models." + rel_modelname )
                    rel_model_instance = getattr(module, str.capitalize(rel_modelname) )()
                    print("removing relation (belongs_to): ", rel_modelname, " -> ", self.modelname)
                    rel_model_instance.remove_relation(self)
                    rel_model_instance.create_schema()
                except Exception as e:
                    raise e    
            # belongs_to
            elif rel_modelname in self.relations.keys():
                print("actually del the relation (belongs_to): ", self.modelname, " -> ", rel_modelname)
                del self.relations[rel_modelname]
                del self.schema[rel_modelname+"_id"]
            # write the new schema and relation json.
            try:
                self.create_schema()
            except Exception as e:
                raise e
            return
        except ImportError as error:
            # Display error message
            print("POWError: unable to import module: %s, error msg: %S " % (rel_modelname, error.message))
            raise error


    def add_column(self, name, attrs={}):
        """ adds a column to this collection. Updates all docs in the collection.
            This might take some time in large collectgions since all docs are touched.
        """
        print("Apennding column to table: %s" % (self.modelname))
        return self.collection.update({},{"$set" : {name: attrs["default"]}},{ "multi": True })

    def add_index(self, *args, **kwargs):
        """ adds an index to a column 
            example: coll.create_index("title", name="title_index_khz", unique=True)
        """
        return self.collection.ensure_index(*args, **kwargs)

    def remove_column(self, name, filter={}):
        """ removes a column 
            see: http://docs.mongodb.org/manual/core/update/#Updating-%24unset
        """
        return self.collection.update(filter, { "$unset": { name : 1 }}, { "multi": True })

    def remove_index(self, name):
        """ removes an index"""
        return self.collection.drop_index({name : 1})

    def rename_column(self, name, new_name, filter={}):
        """ renames a column """
        self.collection.update( filter, { "$rename": { name : new_name }}, { "multi": True } )

    def alter_column_name(self, colname, newname):
         """ alters a column name.
            #TODO Not implemented yet
         """

         print("not implemented yet")
         return False

    def create_table(self, *args, **kwargs):
        """ creates this collection explicitly. Even this is
            not neccessary in mongoDB"""
        #db.createCollection(name, {capped: <boolean>, autoIndexId: <boolean>, size: <number>, max: <number>} )
        # exmaple: db.createCollection("log", { capped : true, size : 5242880, max : 5000 } )
        return self.db.create_collection(self.collection_name, *args, **kwargs)

    def drop(self):
        """ drops this collection / table """
        return self.db.drop_collection(self.collection_name)

    def index_information():
        """Get information on this collections indexes."""
        return self.collection.index_information()
    
    def create_schema(self, prefix_output_path=""):
        """ create a schema for this model
            Automatically add the following column:

            last_updated    ->      by copow
            create          ->      by copow
            _id             ->      by mongodb

        """
        try:
            filepath = prefix_output_path + "./migrations/schemas/" + self.modelname + "_schema.py"
            filepath = os.path.abspath(os.path.normpath(filepath))
            #print filepath
            ofile = open(filepath, "w")
            ostr = self.modelname + " = "
            schema = self.schema
            schema["last_updated"] = { "type" :  "date"  }
            #schema["created"] = { "type" :  "date"  }
            schema["_id"] = { "type" :  "ObjectId"  }
            ostr += json.dumps(schema, indent=4) + powlib.newline 
            ostr += self.modelname + "_relations = "
            ostr += json.dumps(self.relations, indent=4)
            #print(ostr)
            ofile.write(ostr)
            ofile.close()
            self.load_schema()
            self.setup_properties()
        except Exception as e:
            raise e
        return self


