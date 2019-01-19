#coding=utf-8

import inspect
import json
from message import data_type
import bson
import collections
MY_STRING = 1
MY_STRIP_STRING = 2
MY_INT32 = 3
MY_UINT32 = 4
MY_INT16 = 5
MY_UINT16 = 6
MY_CHAR = 7
MY_UCHAR = 8
MY_INT64 = 9
MY_UINT64 = 10
MY_BOOL = 11
MY_DATE = 12
MY_DATETIIME = 13
MY_TIME = 14
MY_FLOAT = 15
MY_BINARY = 16
DATA_TYPE = [int, str, bool]
"""
note: python3: 'dict' object has no attribute 'iterkeys' and 'iteritems'
                use 'keys' and 'items' instead 
"""

class SerializableObj:
    """
    Class: SerializableObj
    Description:the base class of JsonSerializableObj and BsonSerializableObj
    """
    __ATTR_DEF__ = None
    
    def __init__(self):
        pass

    def init_all_attr(self):
        """
        Method:    init_all_attr
        Description: default attr is None,Automatically construct all attributes
                    according to the attribute name defined in  __ATTR_DEF__
        Parameter: none
        Return: 
        Others: 
        """

        for attr_name in self.__ATTR_DEF__.keys():
            setattr(self, attr_name, None)

    def __repr__(self):    
        values = []
        for attr_name in self.__ATTR_DEF__.keys():
            attr_value = getattr(self, attr_name)
            values.append("%s:%r" % (attr_name, attr_value))

        return "%s{%s}" % (self.__class__.__name__, ",".join(values))

    def to_ordered_dict(self):
        """
        Method:    to_ordered_dict
        Description: construct bson or json dict according to __ATTR_DEF__
        Return: dict
        Others: class(serialize) or attr
        """

        attr_defs = self.__ATTR_DEF__

        dict_list = []
        index = 0
        for attr_name, attr_type in attr_defs.items():
            v = getattr(self, attr_name)
            index += 1
            
            if v is None:
                dict_list.insert(index, (attr_name, v))
                continue
                
            if data_type.MY_STRING <= attr_type <= data_type.MY_FLOAT:
                dict_list.insert(index, (attr_name, v))
                continue            
            
            if attr_type == data_type.MY_BINARY:
                dict_list.insert(index, (attr_name, self._gen_bin_value(attr_name, v)))
                continue
                
            if isinstance(attr_type, dict):
                dict_list.insert(index, (attr_name, v))
                continue

            if isinstance(attr_type, list):
                # empty list pass
                if len(attr_type) == 0:
                    dict_list.insert(index, (attr_name, v))
                    continue

                item_type = attr_type[0]

                # List recursion
                if inspect.isclass(item_type) and issubclass(item_type, SerializableObj):                     
                    tmp = [item.to_dict() if item is not None else None for item in v]
                    dict_list.insert(index, (attr_name, tmp))
                    continue

                dict_list.insert(index, (attr_name, v))
                continue

            dict_list.insert(index, (attr_name, v.to_ordered_dict()))

        dict_value = collections.OrderedDict(dict_list)
        return dict_value

    def to_dict(self):
        """
        Method:    to_dict
        Description: to dict
        Others: class or attr
        """

        attr_defs = self.__ATTR_DEF__
        dict_value = {}

        for attr_name, attr_type in attr_defs.items():
            v = getattr(self, attr_name)

            if v is None:
                dict_value[attr_name] = v
                continue

            # if type(data_type) in DATA_TYPE:
            #     dict_value[attr_name] = v
            #     continue
            # if type(attr_type) in DATA_TYPE:
            #     print(attr_type, type(attr_type))

            if isinstance(attr_type, int):
                dict_value[attr_name] = v
                continue

            if isinstance(attr_type, str):
                dict_value[attr_name] = v
                continue

            if isinstance(attr_type, bool):
                dict_value[attr_name] = v
                continue

            if attr_type == data_type.MY_BINARY:
                dict_value[attr_name] = self._gen_bin_value(attr_name, v)
                continue
                
            if isinstance(attr_type, dict):
                dict_value[attr_name] = v
                continue

            if isinstance(attr_type, list):
                if len(attr_type) == 0:
                    dict_value[attr_name] = v
                    continue

                item_type = attr_type[0]

                if inspect.isclass(item_type) and issubclass(item_type, SerializableObj):                     
                    tmp = [item.to_dict() if item is not None else None for item in v]
                    dict_value[attr_name] = tmp
                    continue

                dict_value[attr_name] = v
                continue

            dict_value[attr_name] = v.to_dict()

        return dict_value

    @classmethod
    def from_dict(cls, dict_value):
        """
        Method:    from_dict
        Description: dict to class
        Parameter: dict_value: class attr
        Return: class
        Others: 
        """

        if dict_value is None:
            return None
            
        attr_defs = cls.__ATTR_DEF__
        obj = cls()

        dict_value_get = dict_value.get
        
        for attr_name, attr_type in attr_defs.items():
            v = dict_value_get(attr_name)
            if v is None:
                setattr(obj, attr_name, v)
                continue
            
            if data_type.MY_INT32 <= attr_type <= data_type.MY_FLOAT:
                setattr(obj, attr_name, v)
                continue
                
            if attr_type == data_type.MY_STRING:
                setattr(obj, attr_name, v.encode("utf-8"))
                continue

            if attr_type == data_type.MY_STRIP_STRING:
                setattr(obj, attr_name, v.encode("utf-8").strip())
                continue
                
            if attr_type == data_type.MY_BINARY:
                setattr(obj, attr_name, cls._prase_bin_value(attr_name, v))
                continue
            
            if isinstance(attr_type, dict):
                setattr(obj, attr_name, v)
                continue

            if isinstance(attr_type, list):
                if len(attr_type) == 0:
                    setattr(obj, attr_name, v)
                    continue

                item_type = attr_type[0]

                if item_type == data_type.MY_STRING:
                    item_value = [str_item.encode("utf-8") if str_item is not None else None for str_item in v]
                    setattr(obj, attr_name, item_value)
                    continue

                if item_type == data_type.MY_STRIP_STRING:
                    item_value = [str_item.encode("utf-8").strip() if str_item is not None else None for str_item in v]
                    setattr(obj, attr_name, item_value)
                    continue

                if inspect.isclass(item_type) and issubclass(item_type, SerializableObj):                     
                    tmp = [item_type.from_dict(item) for item in v]
                    setattr(obj, attr_name, tmp)
                    continue

                setattr(obj, attr_name, v)
                continue

            setattr(obj, attr_name, attr_type.from_dict(v))

        return obj

    @classmethod
    def _prase_bin_value(cls, attr_name, value):
        """
        Method:    _prase_bin_value
        Description: prase binary value
        Parameter: 
            attr_name: atrr name
            value: attr value
        Return: 
        Others: bson binary
        """

        pass

    @classmethod
    def _gen_bin_value(cls, attr_name, value):
        pass
        
    def serialize(self):
        pass

    @classmethod
    def deserialize(cls, bin_value):
        pass


class JsonSerializableObj(SerializableObj):
    """
    Class: JsonSerializableObj
    Description: Json serialize
    Base:    SerializableObj 
    Others: 
    """

    @classmethod
    def _prase_bin_value(cls, attr_name, value):

        return value

    @classmethod
    def _gen_bin_value(cls, attr_name, value):

        return value

    def serialize(self):
        dict_value = self.to_dict()
        return json.dumps(dict_value, separators = (',', ':'))
    
    def serialize_ordered(self):
        ordered_dict_value = self.to_ordered_dict()
        return json.dumps(ordered_dict_value, separators = (',', ':'))

    @classmethod
    def deserialize(cls, bin_value):

        if bin_value is None:
            return None
            
        dict_value = json.loads(bin_value)   
        return cls.from_dict(dict_value)


class BsonSerializableObj(SerializableObj):

    @classmethod
    def _prase_bin_value(cls, attr_name, value):
        return str(value)

    @classmethod
    def _gen_bin_value(cls, attr_name, value):
        return bson.Binary(value)

    def serialize(self):

        dict_value = self.to_dict()
        return bson.BSON.encode(dict_value)

    @classmethod
    def deserialize(cls, bin_value):

        if bin_value is None:
            return None

        dict_value = bson.BSON(bin_value).decode()
        return cls.from_dict(dict_value)









