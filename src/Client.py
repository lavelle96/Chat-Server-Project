import threading
import config as cf
from Responses import helo_response, join_response

class client:
    
   
    def __init__(self, socket, address, join_id):
        
        self.name = ""
        self.address = address
        self.socket = socket
        self.port = cf.SERVER_PORT
        self.ip = cf.SERVER_IP
        self.join_id = join_id
    
  

    def set_name(self, name):
        self.name = name
    def set_join_id(self, join_id):
        self.join_id = join_id

        
