import os
import uuid
from cryptography.hazmat.primitives import hashes
#from . import db

class Login(object):
    connection = None
    
    def __init__(self, access=None):
        self.connection = access

    def HashPass(self, password=None, salt=None):
        salted_pass = bytearray(password , 'UTF-8') + salt
        digest = hashes.Hash(hashes.SHA256())
        digest.update(salted_pass)
        return digest.finalize()
    
# Check username field for user & email
    def UserValidate(self, username=None, password=None):
        users = self.connection.SearchUser(username)
        salted_pass = None
        user_uuid = None
        for x in range(0, users.__len__()-1):
            salted_pass = self.HashPass(password, users[x][2])
            if salted_pass == users[x][3]:
                user_uuid = users[x][0]
                break
        return user_uuid
    
    def UserAdd(self, username=None, password=None, email=None):
        salt = os.urandom(32)
        user_uuid = uuid.uuid4().hex
        
        # hash COMB
        hash = self.HashPass(password, salt)
        
        # SQL ADD, user, pass, salt, hash, email
        # dummy command
        command = "INSERT INTO userLogin(user_UUID, username, email, salt, secret) VALUES ("
        command += "x'" + user_uuid + "', '"
        command += username + "', '"
        command += email + "', x'"
        command += salt.hex() + "', x'"
        command += hash.hex() + "')"
        
        
        # NOTE: limit username length
        
        print(command)
        
        print(self.connection.execute_com(command, True))
        
        return command
