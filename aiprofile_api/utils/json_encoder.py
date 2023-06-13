from datetime import datetime, date
from json import JSONEncoder

#from flask.json import JSONEncoder
from bson import ObjectId


# define a custom encoder point to the json_util provided by pymongo (or its dependency bson)
class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        # if object is datetime then return as date object
        if isinstance(o, (datetime, date)):
            return o.isoformat()

        # if format as object id then convert it to string prevent error serialize object
        if isinstance(o, ObjectId):
            return str(o)

        # otherwise return as default data type
        return super().default(o)
