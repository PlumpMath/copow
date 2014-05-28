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


from atest.lib.db_conn import DBConn
#from atest.migrations.schemas.version import version as schema
from atest.migrations.schemas import version_schema as schema_module
import atest.migrations.schemas.version_schema
from atest.lib import powlib
from atest.lib.powlib import _log


newline = powlib.newline
tab = powlib.tab

class BaseModel(object):
    
    #def __init__(self, data=None, schema=None):
    def __setitem__(self, key, value):    
        if key in self.schema.keys():
            setattr(self, key, value)
        else:
            raise Exception( "POWError: model %s has no column %s" % (self.modelname, column) )
        return 

    def set_data(self, data):
        """ set the data for this model from given dictionary data"""
        for key in list(data.keys()):
            if key in self.schema:
                self.__dict__[key] = data[key]
            else:
                raise Exception("unknown attribute: %s for model: %s ") (key, self.modelname)   


    def setup_relations(self):
        for rel_model in list(self.relations.keys()):
            # check relation type
            print("setting up relation for: %s " % (rel_model))
            if self.relations[rel_model] == "has_many":
                mod = importlib.import_module(
                        "atest.models." + powlib.singularize(rel_model) 
                        )
                mod = mod.__dict__[powlib.p2c(rel_model)]
                self.related_models[rel_model] = mod
            else:
                raise Exception("unknown relation: %s ") %(self.relations[rel_mdoel])

    def load_schema(self):
        try:
            """Tries to find the according schema in migrations/schemas/Version.py 
            imports the schema and sets the according properties in this class/instance"""
            #from atest.migrations.schemas.version_schema import version as schema
            #from atest.migrations.schemas.version_schema import version_relations as relations
            which = "atest.migrations.schemas." + self.modelname + "_schema"
            schema = imp.reload(eval(which))
            #print(schema)
            #print(self.modelname), 
            #print(schema.__dict__.keys)
            self.schema = schema.__dict__[self.modelname]
            self.relations = schema.__dict__[self.modelname + "_relations"]
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
            if att_type in powlib.schema_types:
                #print "setting up property for: %s" % (column)
                #setting the according attribvute and the default value, if any.
                setattr(self, column, powlib.schema_types[att_type])
                setattr(self, column+"_type", att_type)
            else:
                raise Exception("no or unknown type given in schema: version_schema.py")
        #self.setup_relations()

    


    def generate_accessor_methods(self):
        """generates the convenient getAttribute() and setAttribute Methods
        and sets them as accessors for this models Attributes """
        for item in list(self._schema.keys()):
            mstr = ""
            self.has_accessor_methods = True
            #getter
            mstr = ""
            method_name = "get_"+ item
            setter = method_name
            tmp_meth_name = "foo"
            mstr +=     "def foo(self):" + newline
            mstr += tab + "return self." + str(item) + newline
            #print mstr
            exec(mstr)
            self.__dict__[method_name] = types.MethodType(foo,self)
            
            
            # setter
            mstr = ""
            method_name = "set_"+ item
            getter = method_name
            tmp_meth_name = "foo"
            mstr +=     "def foo(self, value):" + newline
            mstr += tab + "self." + str(item) + " = value " + newline
            #print mstr
            exec(mstr)
            self.__dict__[method_name] = types.MethodType(foo,self)
        

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
        """ Find all matching models. Returns an iterable."""
        return self.find(*args,**kwargs)
    
    def find(self, *args, sort=None, **kwargs):
        """ Find all matching models. Returns an iterable.
            sorting can be done by giving for exmaple: 
            sort=[("field", pymongo.ASCENDING), ("field2", pymongoDESCENDING),..]
        """
        if sort:
            res = self.collection.find(*args, **kwargs).sort(sort)
        else:
            res = self.collection.find(*args, **kwargs)
        return res

    def find_one(self, *args, **kwargs):
        """ Uses pymongo  find_one directly"""
        ret = self.collection.find_one(*args, **kwargs)
        return ret

    def save(self):
        """ Saves the object. Results in insert if object wasnt in the db before,
            results in update otherwise"""
        d = self.to_json()
        d["last_updated"] = powlib.get_time()
        self._id = self.collection.save(d)
        return self._id

    def insert(self):
        """ Uses pymongo insert directly"""
        d = self.to_json()
        d["last_updated"] = powlib.get_time()
        d["created"] = powlib.get_time()
        self._id = self.collection.insert(d)
        return self._id
        
    def create(self):
        """ Alias for insert()"""
        return self.insert()

    def update(self, *args, **kwargs):
        """  Pure: pymongo update. Can update any document in the collection (not only self)
            Syntax: db.test.update({"x": "y"}, {"$set": {"a": "c"}}) """
        ret = self.collection.update(*args, **kwargs)
        return ret
    
    def update_self(self, val):
        """ Same as : update({"_id": self._id}, val) 
            val must be a dict { key : val1, key : val2 ...}
            always multi=False
        """
        ret = self.collection.update({"_id": self._id}, {"$set": val}, multi=False)
        return ret

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


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        ostr = ""
        for key,val in self.to_json():
            ostr += key + " -> " + val + os.newline 
        return ostr

    def has_many(self, rel_model, embedd=True, one_to_one=False):
        """ creates an (currently embedded) one:many relation between this (self) and model.
            0. check if model exists 
            1. check if relations is not already existing
            2. a list of models is added to self.schema (migrations/schemas)
            3. add the according relation to model_relations dictionary in migrations/schemas
            If one_to_one is set to true this will create a 1:1 relation.
        """
        if type(rel_model) == str:
            rel_modelname = rel_model
        else:
            rel_modelname = rel_model.modelname
        try:
            # 0. check if model exists
            module = importlib.import_module("atest.models." + rel_modelname)
            schema = reload(schema_module)
            self.relations = schema.__dict__[self.modelname+"_relations"]
            # 1. check if relation is not already existing
            if powlib.plural(rel_modelname) in self.relations:
                raise Exception( "POWError: model %s already has a relation to %s " % (self.modelname, rel_modelname) )
                return
            # 2. add list of related model to relations
            if one_to_one:
                print("making a 1:1 relation")
                self.relations[powlib.plural(rel_modelname)] = "has_one"
                self.schema[rel_modelname] = { "type" : "object" }
            else:
                print("making a 1:many relation")
                self.relations[powlib.plural(rel_modelname)] = "has_many"
                self.schema[powlib.plural(rel_modelname)] = { "type" : "list" }
            try:
                filepath = "./migrations/schemas/" + self.modelname + "_schema.py"
                filepath = os.path.abspath(os.path.normpath(filepath))
                #print filepath
                ofile = open(filepath, "w")
                ostr = self.modelname + " = "
                ostr += json.dumps(self.schema, indent=4) + powlib.newline 
                ostr += self.modelname + "_relations = "
                ostr += json.dumps(self.relations, indent=4)
                #print ostr
                ofile.write(ostr)
                ofile.close()
                self.setup_properties()
            except Exception as e:
                raise e
            if one_to_one:    
                self.log("info","%s now has one: %s" %(self.modelname, rel_modelname))
            else:
                self.log("info","%s now has many: %s" %(self.modelname, powlib.pluralize(rel_modelname)))
        except ImportError as error:
            # Display error message
            print("POWError: unable to import module: %s, error msg: %S " % (rel_modelname, error.message))
            raise error

    def has_one(self, model, embedd=True):
        """ creates an (currently embedded) one:one relation between this (self) and model."""
        return self.has_many(model, embedd, one_to_one=True)
            
    def remove_relation(self, rel_model):
        """ tries to find the given relation by its name and deltes the relation entry and the
            instance and class attribute, as well."""
        if type(rel_model) == str:
            rel_modelname = rel_model
        else:
            rel_modelname = rel_model.modelname
        try:
            # 0. check if model exists
            module = importlib.import_module("atest.models." + rel_modelname)
            schema = reload(schema_module)
            self.relations = schema.__dict__[self.modelname+"_relations"]
            # 1. check if relation is existing
            if powlib.plural(rel_modelname) not in self.relations:
                raise Exception( "POWError: model %s already norelation to %s " % (self.modelname, rel_modelname) )
                
            # 2. remove the relation 
            if self.relations[powlib.plural(rel_modelname)] == "has_one":
                del self.relations[powlib.plural(rel_modelname)]
                del self.schema[rel_modelname]
            elif self.relations[powlib.plural(rel_modelname)] == "has_many":
                del self.relations[powlib.plural(rel_modelname)]
                del self.schema[powlib.plural(rel_modelname)]
            # write the new schema and relation json.
            try:
                filepath = "./migrations/schemas/" + self.modelname + "_schema.py"
                filepath = os.path.abspath(os.path.normpath(filepath))
                #print filepath
                ofile = open(filepath, "w")
                ostr = self.modelname + " = "
                ostr += json.dumps(self.schema, indent=4) + powlib.newline 
                ostr += self.modelname + "_relations = "
                ostr += json.dumps(self.relations, indent=4)
                #print ostr
                ofile.write(ostr)
                ofile.close()
                self.setup_properties()
            except Exception as e:
                raise e
            self.log("info","remove relation: %s " % (rel_modelname))
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

    def create_table(self):
        """ creates this collection explicitly. Even this is
            not neccessary in mongoDB"""
        return self.db.create_collection(self.collection_name)

    def drop(self):
        """ drops this collection / table """
        return self.db.drop_collection(self.collection_name)

    def index_information():
        """Get information on this collections indexes."""
        return self.collection.index_information()
    
    def create_schema(self, prefix_output_path=""):
        """ created a schema for this model"""
        try:
            filepath = prefix_output_path + "./migrations/schemas/" + self.modelname + "_schema.py"
            filepath = os.path.abspath(os.path.normpath(filepath))
            #print filepath
            ofile = open(filepath, "w")
            ostr = self.modelname + " = "
            ostr += json.dumps(self.schema, indent=4) + powlib.newline 
            ostr += self.modelname + "_relations = "
            ostr += json.dumps(self.relations, indent=4)
            #print ostr
            ofile.write(ostr)
            ofile.close()
            self.setup_properties()
        except Exception as e:
            raise e
        return self


