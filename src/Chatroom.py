import logging as l
from Client import client
from Responses import join_response
import config as cf
from Format import chat_format
from Responses import leave_response
import threading
l_pre = 'CHATROOM:'

class chatroom:

    def __init__(self, room_reference, chatroom_name):
        l.basicConfig(filename='Server.log',level=l.DEBUG)
        self.room_reference = room_reference
        #client name: join id
        self.join_ids = dict()
        self.chatroom_name = chatroom_name
        self.mutex = threading.Lock()
        """(Client name: Client Objects])"""
        self.connected_clients = dict()
        
   
    def manage_client_join_and_response(self, active_client):
        """Adds client to current connected_clients array and sends a confirmaion message back to the client"""
        l.info(l_pre + 'managing client and join response for client name:' + active_client.name)

        self.mutex.acquire()
        self.connected_clients[active_client.name] = active_client
        self.join_ids[active_client.name] = active_client.join_id
        self.mutex.release()
        message_to_send = join_response(self.chatroom_name, str(cf.SERVER_IP), str(active_client.address[1]), str(self.room_reference), str(active_client.join_id))
        active_client.socket.send(message_to_send.encode('utf-8'))
        self.mutex.acquire()
        self.send_message_to_connected_clients(active_client.name + " has joined the chatroom", active_client)
        self.mutex.release()
        

    def send_message_to_connected_clients(self, message, active_client):
        """Sends given message to every connected client in the chat room"""
        l.info(l_pre + 'sending '+ message + ' to connected clients')
       
        if(not(self.is_client_in_chatroom(active_client))):
            l.warning(l_pre + 'client: ' + active_client.client_name + ' unauthorised to send message to this chatroom')
            self.mutex.release()
            return
        message_to_send = chat_format(str(self.room_reference), active_client.name, message)
        for client_name in self.connected_clients:
            #if not(client[0] == client_name and client[1] == int(join_id)):
            l.info(l_pre + 'sending message to ' + client_name)
            self.connected_clients[client_name].socket.send(message_to_send.encode('utf-8'))
        


    def is_client_in_chatroom(self, active_client):
        """Checks whether or not a given client is in the chat room"""
        if active_client.name in self.connected_clients:
            return True
        return False

    def remove_client_from_chatroom(self, client_name, join_id):
        print('testing ids: client_name: ', client_name, 'join_id', join_id)
        print('names in chatroom: ', self.join_ids.keys())
        if (client_name in self.join_ids) and (str(self.join_ids[client_name]) == str(join_id)):
            print('id match, client name: ', client_name, 'join_id: ', join_id)
            response = leave_response(self.room_reference, self.join_ids[client_name])
            message_to_clients = client_name + ' has left this chatroom'
            self.mutex.acquire()
           
            
            self.send_message_to_connected_clients(message_to_clients, self.connected_clients[client_name])
            self.connected_clients[client_name].socket.send(response.encode(cf.ENCODING_SCHEME))
            self.mutex.release()
            
            self.mutex.acquire()
            del(self.connected_clients[client_name])
            del(self.join_ids[client_name])
            self.mutex.release()
            
            return True

        return False
            
