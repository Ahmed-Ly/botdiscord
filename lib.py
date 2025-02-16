import sys
import json
import requests

# from django.conf import settings

# class MTA():
#     def __init__(self):
#         self.http_username = settings.MTA['USER']
#         self.http_password = settings.MTA['PASSWORD']
#         self.host = settings.MTA['HOST']
#         self.port = settings.MTA['PORT']
#         self.resources = []

class MTA():
    def __init__(self, username, password, host, port):
        self.http_username = username
        self.http_password = password
        self.host = host
        self.port = port
        self.resources = []

    def getResource(self, resourceName):
        '''
        Returns resource object from name
        '''
        for resource in self.resources:
            if resource.getName() == resourceName:
                return resource
        res = Resource(resourceName, self)
        self.resources.append(res)
        return res

    def getInput(self):
        '''
        make the object model from standard input
        '''
        out = self.convertToObjects(json.loads(''.join(sys.stdin.readlines())))
        if type(out) is list:
            return out
        else:
            return None

    @staticmethod
    def doReturn(*args):
        return MTA.convertFromObjects(list(args))

    def callFunction(self, resourceName, function, *args):
        '''
        send function request to game server
        '''
        result = self.do_post_request(
            '/' + resourceName + '/call/' + function,
            json_data=json.dumps(self.convertToObjects(args))
        )
        if result:
            result = json.loads(result)
        else:
            return None
        if type(result) is list:
            return self.convertToObjects(result)
        else:
            return None

    def convertToObjects(self, item):
        '''
        item parameter is a complex object composed of dictonaries, arrays, strings
        here traverse over object model and replace element names with Element objects
        and resource names with Resource objects
        '''
        if type(item) is dict:
            return {key: self.convertToObjects(value) for key, value in item.items()}
        if type(item) is list:
            return [self.convertToObjects(i) for i in item]
        if type(item) is str and item.startswith('^E^'):
            return Element(item[3:])
        if type(item) is str and item.startswith('^R^'):
            return self.getResource(item[3:])
        return item

    @staticmethod
    def convertFromObjects(item):
        '''
        reversed convertToObjects method. replaces Element and Resource
        objects with their names prefixed by corresponing tag: ^E^ or ^R^
        '''
        if type(item) is dict:
            return {key: MTA.convertFromObjects(value) for key, value in item.items()}
        if type(item) is list:
            return [MTA.convertFromObjects(i) for i in item]
        if type(item) is Element:
            return str(item)
        if type(item) is Resource:
            return str(item)
        return item

    def do_post_request(self, path, json_data = ''):
        '''
        make a request to game server,
        using login and password stored in this client object
        '''
        try:
            response = requests.post('http://%s:%s%s' % (self.host, self.port, path),
                  data = json_data,
                  auth = (self.http_username, self.http_password) )
        # this catch may be omited if no need to distinguish connection error
        # (next catch will consume this exception if omited)
        except Exception:
            raise
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code, response.reason)
        return None

class Element():
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return '^E^' + self.id

class Resource():
    def __init__(self, name, server):
        self._name = name
        self._server = server

    def __str__(self):
        return '^R^' + self._name

    def getName(self):
        return self._name

    def call(self, function, *args):
        return self._server.callFunction(self._name, function, *args)

#
# This is a test area. May be safely removed.
#
if __name__ == '__main__':
    from pprint import pprint

    mta = MTA()

    objects = mta.convertToObjects(
        [ { 'x': [ '^E^x', 'Y'], 'y': { 'r': '^R^gold' } } ]
    )

    pprint(objects)

    pprint(MTA.convertFromObjects(objects))

    print(MTA.doReturn('^R^gold', 'sand'))

    mta.http_username = 'website'
    mta.http_password = 'hi'
    mta.host = '127.0.0.1'
    mta.port = '22005'

    pprint(mta.callFunction('usercontrolpanel', 'getServerStats'))
    pprint(mta.getResource('webadmin').call('getGroups'))

    pprint(mta.getInput())
