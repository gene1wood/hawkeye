#!/use/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import xmltodict


# This makes a dict act like an auto-vivicating perl hash
# Keeping here now because this is the only place I'm using it
class PerlStyleHash(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


# Note:  This is a class because it's intended to have more functionality later
class HawkeyeParse:
    def __init__(self):
        self._boto_objects = PerlStyleHash()  # This is OK as a global
        return self

    def parse(self, obj, logger=None):
        """ Takes results from boto and parses it into a normalized
        dict-of-dicts. This can also take an array or dict of boto query
        objects and normalize it to a dict of dicts """

        self._parser(obj)  # we don't care about the return data here
        self._post_process()
        return self._boto_objects

    def _parser(self, obj, depth=0):
        """ The root of our recursive parser
        input:
            object: (required) the object to parse
            depth:  (optional) the current depth of recursion

        output:
            normalized results of what we parsed"""

        obj_type = _get_obj_type(obj)

        if obj_type in self._parse_table:
            # We designated a specific parser for this object type
            # A pointer to the method is held within a dict of object types
            ret = self._parse_table[obj_type](self, obj, depth=depth)
        else:
            # No designated parser means we treat it like a boto object.
            # Todo:  create list of known/expected objects for boto
            #        Then log on new object types
            ret = self._parse_boto(obj, obj_type, depth=depth)
        return ret

    def _parse_none(self, obj, depth=0):
        """ Always return None; Handy for eliminating objects we don't want
        results for. """

        return None

    def _parse_list(self, obj, depth=0):
        """ Recursivly parses lists, then returns the parsed de-duped results. """

        ret = []
        for item in obj:
            ret.append(self._parser(item, depth=depth))
        return list(set(ret))

    def _parse_simple(self, obj, depth=0):
        """ Return the object sent to us, no further parsing needed """

        return obj

    def _parse_name(self, obj, depth=0):
        """ returns the object as a string. Often a simple way to convert to
        human readable form """

        return str(obj)

    def _parse_timedelta(self, obj, depth=0):
        """ converts timedelta to seconds """

        return str(obj.total_seconds()) + " seconds"

    def _parse_dict(self, obj, depth=0):
        """ Recursivly parses dicts, returns results. """

        ret = {}
        for key, value in obj.iteritems():
            value = self._parser(value, depth=depth)
            if value is not None:
                ret[key] = value
        return ret

    def parse_custom_dict(obj, fields):
        """ Convert simple objects directly to a dict """
        ret = dict()
        props = dir(obj)
        for item in fields:
            if item in props:
                ret[item] = getattr(obj,item)
                return ret


    def _get_object_id(self, obj, obj_type):
        """ Helper function to normalize object unique id's for our dict of
        dicts """

        array = dir(obj)
        if 'id' in array:
            # Object has an ID field
            ret = getattr(obj, 'id')
        elif 'name' in array:
            # Object doesn't have an ID, but has a name
            ret = getattr(obj, 'name')
        elif obj_type in _boto_object_id:
            # We have an ID generator for the object
            ret = _boto_object_id[obj_type](obj)
        else:
            # we only get here if we don't know what to do
            print "No ID Fields:", obj_type, obj, _obj_to_dict(obj)
            ret = "None"
        return str(ret)

    def _get_obj_type(self, obj):
        """ Helper function to create a normalized object type as a string """

        return str(type(obj).__name__)

    def _obj_to_dict(self, obj):
        """ Helper function to convert any given object's properties and
        methods to a dict to aid in inspection """

        return dict((name, getattr(obj, name)) for name in dir(obj) if not name.startswith('_'))

    def _parse_boto(self, obj, obj_type, depth=0):
        """ Parse boto objects and put their results into self._boto_objects
        dict of dicts.

        Returns:
            A text based reference pointer to the object as it's listed in the
            self._boto_objects tree.  This is because there are a significant
            number of circular references which cannot be easily converted to
            json.

        For example:
            "Reference:Instance:i-123456" can be found as
            self._boto_objects["Instance"]["i-123456"]"""

        # max recursion only applies to boto objects due to circular refs
        # we still want to recurse a little
        if depth < 5:
            depth += 1
            uniq = _get_object_id(obj, obj_type)
            if not uniq in self.self._boto_objects[obj_type]:
                for name in dir(obj):
                    if not name.startswith('_'):
                        value = getattr(obj, name)
                        data = self._parser(value, depth=depth)
                        if obj_type in _boto_null_ok:
                            self.self._boto_objects[obj_type][uniq][name] = data
                        elif data is not None:
                            self.self._boto_objects[obj_type][uniq][name] = data
            return "Reference:" + obj_type + ":" + uniq
        else:
            return None

    def _post_process(self):
        """ Perform post processing of any known data types that require it.
        Works directly on self._boto_objects"""

        # Todo:  convert "_id" fields to standard reference format
        #        break out into seperate methods when we have more routines

        # VPN configuration data is in XML, so lets convert to a dict of dicts
        for key in self.self._boto_objects["VpnConnection"].keys():
            customer_config = self.self._boto_objects["VpnConnection"][key]["customer_gateway_configuration"]
            xmldict = xmltodict.parse(customer_config)
            self.self._boto_objects["VpnConnection"][key]["customer_gateway_configuration"] = xmldict

    # Simple table of lambda function to create unique ids
    # ToDo:  Get rid of Lambda!
    _boto_object_id = {
        "NetworkAclEntry": lambda obj: ("egress-" if str(obj.egress) == 'true' else "ingress-") + str(obj.rule_number),
        "Route": lambda obj: obj.destination_cidr_block,
        "PortRange": lambda obj: str(obj.from_port) + "-" + str(obj.to_port),
        "VpnTunnel": lambda obj: obj.outside_ip_address,
        "Icmp": lambda obj: str(obj.type) + ":" + str(obj.code),
        "Attachment": lambda obj: obj.vpc_id,
        "Address": lambda obj: obj.public_ip,
        "BlockDeviceType": lambda obj: obj.volume_id,
        "PrivateIPAddress": lambda obj: obj.private_ip_address,
        "IPPermissions": lambda obj: hashlib.md5(str(obj) + " " + str(obj.ip_protocol) + ":" + str(obj.from_port) + "-" + str(obj.to_port)).hexdigest(),
        "RecurringCharge": lambda obj: str(obj.amount) + " " + str(obj.frequency),
        "HealthCheck": lambda obj: obj.target,
        "Listener": lambda obj: obj.get_tuple(),
    }

    # It's important to get null data results for these types only.
    # We don't really want or care about any other nulls
    _boto_null_ok = [
        "PortRange",
        "Icmp",
        "Attachment",
    ]

    # This table of method pointers tells us how we want to parse this object
    # ToDo:  Get rid of Lambda!
    _parse_table = {
        "NoneType": _parse_none,
        "dict": _parse_dict,
        "list": _parse_list,
        "str": _parse_simple,
        "int": _parse_simple,
        "datetime": _parse_simple,
        "timedelta": _parse_timedelta,
        "function": _parse_none,
        "instancemethod": _parse_none,
        "unicode": _parse_simple,
        "ResultSet": _parse_list,
        "ProductCodes": _parse_list,
        "TagSet": _parse_dict,
        "bool": _parse_simple,
        "InstancePlacement": _parse_simple,
        "SubParse": _parse_dict,
        "InstanceState": _parse_name,
        "BlockDeviceMapping": _parse_dict,
        "BillingProducts": _parse_list,
        "VPCConnection": _parse_none,
        "builtin_function_or_method": _parse_none,
        "DhcpConfigSet": _parse_none,
        "InternetGatewayAttachment": _parse_none,
        "EC2Connection": _parse_none,
        "type": _parse_simple,
        "property": _parse_simple,
        "MessageSet": _parse_none,
        "Element": _parse_none,
        "getset_descriptor": _parse_dict,
        "IPPermissionsList": _parse_list,
        "InstanceStatusSet": _parse_list,
        "Details": _parse_dict,
        "Status": lambda obj,depth=0,parent=None: _parse_custom_dict(obj,["status","details"]),
        "RecurringCharge": lambda obj,depth=0,parent=None: _parse_custom_dict(obj,["amount","frequency"]),
        "tuple": _parse_simple,
        "ELBConnection": _parse_none,
        "RDSConnection": _parse_none,
        "S3Connection": _parse_none,
        "ListElement": _parse_list,
        "EventSet": _parse_list,
        "PendingModifiedValues": _parse_dict,
        "Policies": _parse_list,
        "AppCookieStickiness": _parse_list,
        "LBCookieStickiness": _parse_list,
        "Other": _parse_list,
        "ReadReplicaDBInstanceIdentifiers": _parse_list,
        "ReadReplicaDBInstanceIdentifiers": _parse_list,
        "VolumeStatusSet": _parse_list,
        "ActionSet": _parse_list,
        "Event": lambda obj,depth=0,parent=None: _parse_custom_dict(obj,["code","description","not_after","not_before"]),
        "StatusInfo": lambda obj,depth=0,parent=None: _parse_custom_dict(obj,["status","normal","message","status_type"]),
    }
