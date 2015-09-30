# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

"""
Data Module

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

from datetime import datetime
from jsonschema import Draft4Validator
from tornado.util import ObjectDict
from tornado.gen import coroutine
from tornado.gen import Return
from bson import ObjectId
from pymongo import ASCENDING


EXTRA_SCHEMA_TYPES = {
    "datetime":(datetime,),
    "objectid":(ObjectId,)
}


PARTICLE_TYPE_SCHEMA = {
    "title":"Particle Type",
    "type":"object",
    "properties":{
        "_id":{
            "type":"objectid"
        },
        "type":{
            "type":"string"
        },
        "name":{
            "type":"string"
        },
        "protons":{
            "type":"integer"
        },
        "neutrons":{
            "type":"integer"
        }
    }
}


LATTICE_SCHEMA = {
    "title":"",
    "type":"object",
    "properties":{
        "_id":{
            "type":"objectid"
        },
        "lattice_type":{
            "type":"string"
        },
        "particle_type":{
            "type":"string"
        },
        "status_type":{
            "type":"string"
        },
        "name":{
            "type":"string"
        },
        "description":{
            "type":"string"
        },
        "created_by":{
            "type":"string"
        },
        "created_date":{
            "type":"datetime"
        },
        "properties":{
            "type":"array",
            "items":{
                "type":"object",
                "properties":{
                    "name":{
                        "type":"string"
                    },
                    "value":{
                        "type":[ "string", "number", "array"]
                    },
                    "units":{
                        "type":"string"
                    }
                },
                "required":[ "name", "value" ]
            }
        },
        "files":{
            "type":"array",
            "items":{
                "type":"object",
                "properties":{
                    "_id":{
                        "type":"objectid"
                    },
                    "name":{
                        "type":"string"
                    },
                    "filename":{
                        "type":"string"
                    },
                    "location":{
                        "type":"string"
                    }
                },
                "required":[ "_id", "name", "filename", "location" ]
            }
        },
    },
    "required":[ "lattice_type", "particle_type", "status_type",
                "name", "description","created_by", "created_date" ]
}


LATTICE_ELEMENT_SCHEMA = {
    "title":"",
    "type":"object",
    "properties":{
        "order":{
            "type:":"integer"
        },
        "type":{
            "type":"string"
        },
        "lattice_id":{
            "type":"objectid"
        },
        "name":{
            "type":"string"
        },
#         "created_by":{
#             "type":"string"
#         },
#         "created_date":{
#             "type":"datetime"
#         },
        "length":{
            "type":"number"
        },
        "position":{
            "type":"number"
        },
        "properties":{
            "type":"array",
            "items":{
                "type":"object",
                "properties":{
                    "name":{
                        "type":"string"
                    },
                    "value":{
                        "type":[ "string", "number", "array"]
                    },
                    "units":{
                        "type":"string"
                    }
                },
                "required":[ "name", "value" ]
            }
        }
    },
    "required":[ "order",  "type", "name", "length", "position" ]
}


MODEL_SCHEMA = {
    "title":"",
    "type":"object",
    "properties":{
        "_id":{
            "type":"objectid"
        },
        "lattice_id":{
            "type":"objectid"
        },
        "name":{
            "type":"string"
        },
        "description":{
            "type":"string"
        },
        "created_by":{
            "type":"string"
        },
        "created_date":{
            "type":"datetime"
        },
        "properties":{
            "type":"array",
            "items":{
                "type":"object",
                "properties":{
                    "name":{
                        "type":"string"
                    },
                    "value":{
                        "type":[ "string", "number", "array"]
                    },
                    "units":{
                        "type":"string"
                    }
                },
                "required":[ "name", "value" ]
            }
        },
        "files":{
            "type":"array",
            "items":{
                "type":"object",
                "properties":{
                    "_id":{
                        "type":"objectid"
                    },
                    "name":{
                        "type":"string"
                    },
                    "filename":{
                        "type":"string"
                    },
                    "location":{
                        "type":"string"
                    }
                },
                "required":[ "_id", "name", "filename", "location" ]
            }
        },
    },
    "required":[ "lattice_id", "name", "description","created_by", "created_date" ]
}


MODEL_ELEMENT_SCHEMA = {
    "title":"",
    "type":"object",
    "properties":{
        "model_id":{
            "type":"objectid"
        },
        "lattice_element_id":{
            "type":"objectid"
        },
        "properties":{
            "type":"array",
            "items":{
                "type":"object",
                "properties":{
                    "name":{
                        "type":"string"
                    },
                    "value":{
                        "type":[ "string", "number", "array"]
                    },
                    "units":{
                        "type":"string"
                    }
                },
                "required":[ "name", "value" ]
            }
        }
    },
    "required":[ "model_id", "lattice_element_id", ]
}


class MotorDataProvider(object):

    def __init__(self, application):
        self.application = application
        self._particle_type_validator = Draft4Validator(PARTICLE_TYPE_SCHEMA, types=EXTRA_SCHEMA_TYPES)
        self._lattice_validator = Draft4Validator(LATTICE_SCHEMA, types=EXTRA_SCHEMA_TYPES)
        self._lattice_element_validator = Draft4Validator(LATTICE_ELEMENT_SCHEMA, types=EXTRA_SCHEMA_TYPES)
        self._model_validator = Draft4Validator(MODEL_SCHEMA, types=EXTRA_SCHEMA_TYPES)
        self._model_element_validator = Draft4Validator(MODEL_ELEMENT_SCHEMA, types=EXTRA_SCHEMA_TYPES)


    @coroutine
    def validate_particle_type(self, particle_type):
        return self._particle_type_validator.validate(particle_type)


    @coroutine
    def find_particle_types(self):
        db = self.application.db
        particle_types = yield db.particle_type.find().to_list(None)
        raise Return(_bless(particle_types))


    @coroutine
    def find_particle_type_by_id(self, type_id):
        db = self.application.db
        query = { "type":str(type_id) }
        particle_type = yield db.particle_type.find_one(query)
        raise Return(_bless(particle_type))


    @coroutine
    def insert_particle_type(self, particle_type, validate=True):
        if validate:
            self.validate_particle_type(particle_type)
        db = self.application.db
        particle_type_id = yield db.particle_type.insert(particle_type)
        raise Return(particle_type_id)


    @coroutine
    def find_lattice_types(self):
        settings = self.application.settings
        lattice_support = settings.get("lattice_support", [])
        lattice_types = []
        for support in lattice_support:
            lattice_types.append(dict(
                    type=support[0],
                    name=support[1]
            ))
        return lattice_types


    @coroutine
    def find_lattice_type_by_id(self, type_id):
        settings = self.application.settings
        lattice_support = settings.get("lattice_support", [])
        lattice_type = None
        for support in lattice_support:
            if support[0] == type_id:
                lattice_type = dict(
                    type=support[0],
                    name=support[1]
                )
        return lattice_type


    @coroutine
    def find_model_types(self):
        settings = self.application.settings
        model_support = settings.get("model_support", [])
        model_types = []
        for support in model_support:
            model_types.append(dict(
                    type=support[0],
                    name=support[1]
            ))
        return model_types


    @coroutine
    def find_model_type_by_id(self, type_id):
        settings = self.application.settings
        model_support = settings.get("model_support", [])
        model_type = None
        for support in model_support:
            if support[0] == type_id:
                model_type = dict(
                    type=support[0],
                    name=support[1]
                )
        return model_type


    @coroutine
    def validate_lattice(self, lattice):
        return self._lattice_validator.validate(lattice)


    @coroutine
    def find_lattice_by_id(self, lattice_id):
        db = self.application.db
        query = { "_id":ObjectId(lattice_id) }
        lattice = yield db.lattice.find_one(query)
        raise Return(_bless(lattice))


    @coroutine
    def find_lattices(self):
        db = self.application.db
        lattices = yield db.lattice.find().to_list(None)
        raise Return(_bless(lattices))


    @coroutine
    def search_lattices(self, **kwargs):
        query = []

        lattice_type = kwargs.get("lattice_type", None)
        if lattice_type and len(lattice_type) > 0:
            query.append(dict(lattice_type = lattice_type))

        particle_type = kwargs.get("particle_type", None)
        if particle_type and len(particle_type) > 0:
            query.append(dict(particle_type = particle_type))

        lattice_name = kwargs.get("lattice_name", None)
        if lattice_name and len(lattice_name) > 0:
            regex = re.escape(lattice_name)
            regex = regex.replace("\\*", "(.*)")
            regex = regex.replace("\\?", "(.?)")
            query.append(dict(name = { "$regex" : regex, "$options":"i" })) # consider: m

        if len(query) == 0:
            query = {}
        elif len(query) == 1:
            query = query[0]
        else:
            query = { "$and" : query }

        db = self.application.db
        lattices = yield db.lattice.find(query).to_list(None)
        raise Return(lattices)


    @coroutine
    def insert_lattice(self, lattice, validate=True):
        if validate:
            self.validate_lattice(lattice)
        db = self.application.db
        lattice_id = yield db.lattice.insert(lattice)
        raise Return(lattice_id)


    @coroutine
    def validate_lattice_element(self, lattice_element):
        return self._lattice_element_validator.validate(lattice_element)


    @coroutine
    def find_lattice_element_by_id(self, lattice_element_id):
        db = self.application.db
        query = { "_id":ObjectId(lattice_element_id) }
        lattice_element = yield db.lattice_element.find_one(query)
        raise Return(lattice_element)


    @coroutine
    def find_lattice_element_by_name(self, lattice_id, name, order):
        db = self.application.db
        query = {
            "lattice_id":ObjectId(lattice_id),
            "name":name, "order":order
        }
        lattice_element = yield db.lattice_element.find_one(query)
        raise Return(_bless(lattice_element))


    @coroutine
    def find_lattice_element_by_order(self, lattice_id, order):
        db = self.application.db
        query = {
            "lattice_id":ObjectId(lattice_id), "order":order
        }
        lattice_element = yield db.lattice_element.find_one(query)
        raise Return(_bless(lattice_element))


    @coroutine
    def find_lattice_elements_by_lattice_id(self, lattice_id):
        db = self.application.db
        query = { "lattice_id":ObjectId(lattice_id) }
        cursor = db.lattice_element.find(query)
        cursor = cursor.sort("order", ASCENDING)
        lattice_elements = yield cursor.to_list(None)
        raise Return(_bless(lattice_elements))


    @coroutine
    def insert_lattice_element(self, lattice_element, validate=False):
        if validate:
            self.validate_lattice_element(lattice_element)
        db = self.application.db
        lattice_element_id = yield db.lattice_element.insert(lattice_element)
        raise Return(lattice_element_id)


    @coroutine
    def validate_model(self, model):
        return self._model_validator.validate(model)


    @coroutine
    def find_model_by_id(self, model_id):
        db = self.application.db
        query = { "_id":ObjectId(model_id) }
        model = yield db.model.find_one(query)
        raise Return(_bless(model))


    @coroutine
    def find_models(self):
        """Get the list of models.

        :return: list of models
        """
        db = self.application.db
        cursor = db.model.find()
        # should the models be sorted?
        models = yield cursor.to_list(None)
        raise Return(_bless(models))


    @coroutine
    def find_models_by_lattice_id(self, lattice_id):
        """Get the list of models associated with the given lattice_id.

        :param lattice_id: lattice id
        :return: list of models
        """
        db = self.application.db
        query = { "lattice_id":ObjectId(lattice_id) }
        cursor = db.model.find(query)
        # should the models be sorted?
        models = yield cursor.to_list(None)
        raise Return(_bless(models))


    @coroutine
    def search_models(self, **kwargs):
        query = []

        #lattice_type = kwargs.get("lattice_type", None)
        #if lattice_type and len(lattice_type) > 0:
        #    query.append(dict(lattice_type = lattice_type))

        #particle_type = kwargs.get("particle_type", None)
        #if particle_type and len(particle_type) > 0:
        #    query.append(dict(particle_type = particle_type))

        model_name = kwargs.get("model_name", None)
        if model_name and len(model_name) > 0:
            regex = re.escape(model_name)
            regex = regex.replace("\\*", "(.*)")
            regex = regex.replace("\\?", "(.?)")
            query.append(dict(name = { "$regex" : regex, "$options":"i" })) # consider: m

        if len(query) == 0:
            query = {}
        elif len(query) == 1:
            query = query[0]
        else:
            query = { "$and" : query }

        db = self.application.db
        lattices = yield db.model.find(query).to_list(None)
        raise Return(_bless(lattices))


    @coroutine
    def insert_model(self, model, validate=True):
        if validate:
            self.validate_model(model)
        db = self.application.db
        model_id = yield db.model.insert(model)
        raise Return(model_id)


    @coroutine
    def validate_model_element(self, model_element):
        return self._model_element_validator.validate(model_element)


    @coroutine
    def find_model_element_by_id(self, model_element_id):
        db = self.application.db
        query = { "_id":ObjectId(model_element_id) }
        model_element = yield db.model_element.find_one(query)
        raise Return(_bless(model_element))


    @coroutine
    def find_model_elements_by_model_id(self, model_id):
        db = self.application.db
        query = { "model_id":ObjectId(model_id) }
        cursor = db.model_element.find(query)
        cursor = cursor.sort("position", ASCENDING)
        model_elements = yield cursor.to_list(None)
        raise Return(_bless(model_elements))


    @coroutine
    def find_model_elements_property_values(self, model_id, property_name):
        db = self.application.db
        pipeline = [
            { "$match": { "model_id":ObjectId(model_id) }},
            { "$unwind": "$properties" },
            { "$match": { "properties.name":str(property_name) }},
            { "$sort" : { "position":ASCENDING }},
            { "$group": { "_id":"$properties.name",
                "values":{ "$push":"$properties.value" },
                "positions":{ "$push":"$position" }
                }
            }
        ]
        result = yield db.model_element.aggregate(pipeline)
        if not result["ok"]:
            #LOG ERROR
            raise Return([])

        if len(result["result"]) > 1:
            #LOG WARN
            pass

        raise Return(result["result"][0])


    @coroutine
    def insert_model_element(self, model_element, validate=True):
        if validate:
            self.validate_model_element(model_element)
        db = self.application.db
        model_element_id = yield db.model_element.insert(model_element)
        raise Return(model_element_id)



def _bless(obj):
    """Convert collections of standard dictionaries to ObjectDict objects.
    """
    if isinstance(obj, dict):
        blessed = ObjectDict(obj)
        stack = [ blessed ]
    elif isinstance(obj, list):
        blessed = list(obj)
        stack = [ blessed ]
    else:
        blessed = obj
        stack = []

    while len(stack) > 0:
        obj = stack.pop()

        if isinstance(obj, dict):
            for key in obj.keys():
                if isinstance(obj[key], dict):
                    obj[key] = ObjectDict(obj[key])
                    stack.append(obj[key])
                elif isinstance(obj[key], list):
                    obj[key] = list(obj[key])
                    stack.append(obj[key])

        if isinstance(obj, list):
            for idx in xrange(len(obj)):
                if isinstance(obj[idx], dict):
                    obj[idx] = ObjectDict(obj[idx])
                    stack.append(obj[idx])
                elif isinstance(obj[idx], list):
                    obj[idx] = list(obj[idx])
                    stack.append(obj[idx])

    return blessed


