#!/usr/bin/env python3

# Adapted from https://docs.python.org/3/library/xmlrpc.server.html#xmlrpc.server.SimpleXMLRPCServer

# Provide a test for valid username
# Provide a "database" lookup from username to user UUID (and status)
# Illustrate a session concept (implementation is suboptimal)

sessionDatabase = {
        "app1" : "secret1",
        "app2" : "secret2",
        }

userDatabase = {
        "ahmed": {"UUID": "1111111", "activeStatus" : True },
        "jane":  {"UUID": "1111112", "activeStatus" : False },
        "alec": {"UUID": "1111113", "activeStatus" : True },
        }

activeSessions = {}

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.client import Fault
from random import randint

def session(id,sec):
    """Calulate and store a new session id"""
    # Remove stale sessions
    while activeSessions.pop(id,False):
        pass

    activeSessions[id] = id + sec + str(randint(1,1000))
    return activeSessions[id]


def authApp(id, sec):
    """Validate application credetionls and return a sessions ID"""
    if sessionDatabase[id] == sec:
        return session(id,sec)
    else:
        raise Fault(10, "Invalid session credentials")


def validateSess(sess):
    """Validates a session ID"""
    for _, s in activeSessions.items():
        if s == sess:
            return true
    return false


def userExists(sess, u):
    """Does a user exist?"""
    return (u in userDatabase) and userDatabase[u]["activeStatus"] == True


def getActiveUserUUID(sess, u):
    """Get the UUID for given active user"""
    return getUserUUIDbyState(sess, u, "active")


def getUserUUIDbyStatus(sess, u, s):
    """Get the UUID for a given user, any status"""
    if u in userDatabase and userDatabase[u]["activeStatus"] == s:
        return {"user": u, "UUID": userDatabase[u]["UUID"]}
    else:
        raise Fault(1, "No {status} user {user} found".format(status = "active" if s else "inactive", user=u))


def getUserAllDetails(sess, u):
    """Get all the user details for a given active user"""
    if userExists(sess, u):
        result = userDatabase[u]
        result.update({"user": u})
        return result
    else:
        raise Fault(1, "No active user {} found".format(u))


def getAllUsersByStatus(sess, s):
    """List all the users, filtered by their active status"""
    # NOTE: Normally it's bad practice to return a potentially huge list.
    result = []
    for user, info in userDatabase.items():
        if info["activeStatus"] == s:
            info.update({"user": user})
            result.append(info)

    if len(result) == 0:
        raise Fault(2, "No users found with active status of {}".format(s))

    return result



if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/users',)

    # Create server
    with SimpleXMLRPCServer(("localhost", 8080),
                requestHandler=RequestHandler) as server:

        server.register_introspection_functions()
        server.register_function(authApp)
        server.register_function(userExists)
        server.register_function(getActiveUserUUID)
        server.register_function(getUserUUIDbyStatus)
        server.register_function(getUserAllDetails)
        server.register_function(getAllUsersByStatus)

        # Run the server's main loop
        server.serve_forever()

