# from flask.ext.mongoalchemy import MongoAlchemy, Document
# import mongoengine
# def encode_model(obj, recursive=False):
#     if obj is None:
#         return obj
#     if isinstance(obj, (mongoengine.Document, mongoengine.EmbeddedDocument)):
#         out = dict(obj._data)
#         for k,v in out.items():
#             if isinstance(v, ObjectId):
#                 if k is None:
#                     out['_id'] = str(v)
#                     del(out[k])
#                 else:
#                     # Unlikely that we'll hit this since ObjectId is always NULL key
#                     out[k] = str(v)
#             else:
#                 out[k] = encode_model(v)
#     elif isinstance(obj, mongoengine.queryset.QuerySet):
#         out = encode_model(list(obj))
#     elif isinstance(obj, ModuleType):
#         out = None
#     elif isinstance(obj, groupby):
#         out = [ (g,list(l)) for g,l in obj ]
#     elif isinstance(obj, (list)):
#         out = [encode_model(item) for item in obj]
#     elif isinstance(obj, (dict)):
#         out = dict([(k,encode_model(v)) for (k,v) in obj.items()])
#     elif isinstance(obj, datetime.datetime):
#         out = str(obj)
#     elif isinstance(obj, ObjectId):
#         out = {'ObjectId':str(obj)}
#     elif isinstance(obj, (str, unicode)):
#         out = obj
#     elif isinstance(obj, float):
#         out = str(obj)
#     else:
#         raise TypeError, "Could not JSON-encode type '%s': %s" % (type(obj), str(obj))
#     return out

import datetime

class Eastern(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5)

    def tzname(self, dt):
        return "EST"

    def dst(self, dt):
        return datetime.timedelta(0)