#!/usr/bin/env python3

# A smple complete example for the LCA 2018 API

import xmlrpc.client

host = "localhost"
port = "8080"
urlEndPoint="http://"+host+":"+port+"/users"

proxy = xmlrpc.client.ServerProxy(urlEndPoint) 

testUser = "alec" # valid test data

# Create a session id

try:
    sessionID = proxy.authApp("app1","secret1")
    print("Got Session ID {}".format(sessionID))
except xmlrpc.client.Fault as error:
    print("""\nCall to user API failed with xml-rpc fault!
reason {}""".format(
        error.faultString))

except xmlrpc.client.ProtocolError as error:
    print("""\nA protocol error occurred
URL: {}
HTTP/HTTPS headers: {}
Error code: {}
Error message: {}""".format(
        error.url, error.headers, error.errcode, error.errmsg))

except ConnectionError as error:
    print("\nConnection error. Is the server running? {}".format(error))


# Make a couple of simple call to validate a user name
try:
    result = proxy.userExists(sessionID, testUser)
    print("\nCalled userExist() on user {},\nresult {}".format(
        testUser, result))

    result = proxy.getUserAllDetails(sessionID, testUser)
    print("""Called getUserAllDetails() on user {},
UUID is {},
active status is {}""".format(
        testUser, result["UUID"], result["activeStatus"]))

except xmlrpc.client.Fault as error:
    print("""\nCall to user API failed with xml-rpc fault!
reason {}""".format(
        error.faultString))

except xmlrpc.client.ProtocolError as error:
    print("""\nA protocol error occurred
URL: {}
HTTP/HTTPS headers: {}
Error code: {}
Error message: {}""".format(
        error.url, error.headers, error.errcode, error.errmsg))

except ConnectionError as error:
    print("\nConnection error. Is the server running? {}".format(error))

