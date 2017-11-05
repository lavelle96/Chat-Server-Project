import threading
import config as cf
from Responses import helo_response, join_response

class client:
    
   
    def __init__(self, socket, address):
        
        self.name = ""
        self.address = address
        self.socket = socket
        self.port = cf.SERVER_PORT
        self.ip = cf.SERVER_IP
        self.join_ids = dict()
    
  

    def set_name(self, name):
        self.name = name

        
