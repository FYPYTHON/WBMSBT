# coding=utf-8
import json
from datetime import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and
                          x != 'non_db_object']:
                data = obj.__getattribute__(field)
                print(data)
                try:
                    if isinstance(data, datetime):
                        data = data.strftime('%Y-%m-%d %H:%M:%S')
                        json.dumps(data)
                        fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)


def new_alchemy_encoder():
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        print("al ...")
        def default(self, obj):
            print("bl...")
            print(dir(obj))
            print(isinstance(obj.__class__, DeclarativeMeta))
            if isinstance(obj.__class__, DeclarativeMeta):
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)
                fields = {}
                print(dir(obj))
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and
                              x != 'non_db_object']:
                    data = obj.__getattribute__(field)
                    print(data)
                    try:
                        if isinstance(data, datetime):
                            data = data.strftime('%Y-%m-%d %H:%M:%S')
                            json.dumps(data)
                            fields[field] = data
                    except TypeError:
                        fields[field] = None
                return fields
            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder
