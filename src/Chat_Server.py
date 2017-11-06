import threading
from socket import*
import sys
import os
from Chatroom import chatroom
from Message_Parser import parse_join, parse_leave, parse_disconnect, parse_chat
import logging as l
import config as cf
from Client import client
from Responses import helo_response


l_pre = 'CHAT_SERVER:'

class chat_server():
    
    def __init__(self):
        """Set up thread to accept connections"""
        l.basicConfig(filename='Server.log',level=l.DEBUG)
        self.threads = []
        #active_chatrooms structure: ([Chatroom name: Chatroom Object])
        self.active_chatrooms = dict()
        self.current_room_reference = 0
        #self.chatroom_lock = threading.Lock()
        self.server_port = cf.SERVER_PORT
        self.server_socket = socket(AF_INET,SOCK_STREAM)
        self.server_socket.bind(('',self.server_port))
        self.server_socket.listen(5)
        print('The server is ready to receive')
        
        #Setup thread looking for command to quit program
        command_control_thread = threading.Thread(target=self.manage_command_line_input)
        self.threads.append(command_control_thread)
        command_control_thread.start()
    
        while 1:
        #Accept connections from clients and start a new thread handling each new connection
            connection_socket, addr = self.server_socket.accept()
            new_client = client(connection_socket, addr)
            new_connection_thread = threading.Thread(target = self.manage_connection_thread, args = (new_client,))
            self.threads.append(new_connection_thread)
            new_connection_thread.start()
            
        connection_socket.close()



    def manage_connection_thread(self, active_client):
        """Function invoked by new threads managing new connections"""
        l.info(l_pre + 'Managing new connection on new thread')
        
        while 1:
            
            received_data = active_client.socket.recv(4096)
            print('message received')
            #Close socket connection with client if their side is down
            if not received_data:
                print("Closing thread due to lack of data received")
                break
            
            message = received_data.decode()
            print(message)
            message_split = message.split()
             
            if(message_split[0] == 'KILL_SERVICE'):
                self.server_socket.close()
                os._exit(1)
                return
            elif(message_split[0] == 'HELO'):
                self.send_helo_response(message, active_client)
            elif(message_split[0] == 'JOIN_CHATROOM:'):
                self.manage_join(message, active_client)
            elif(message_split[0] == 'CHAT:'):
                self.manage_chat(message, active_client)
            elif(message_split[0] == 'LEAVE_CHATROOM:'):
                self.manage_leave(message, active_client)
                    
        print('connection_finished')
        active_client.socket.close()
        


                
#----------------------FUNCTIONS TO MANAGE CLIENT CALLS----------------------

    def send_helo_response(self, message, active_client):
        """Function called when the input is helo"""
        """Sends a message back to connected client"""
        print("sending hello response")
        text = message.split()[1]
        message_to_send = helo_response(text, cf.SERVER_IP, str(cf.SERVER_PORT), cf.STUDENT_NUMBER)
        active_client.socket.send(message_to_send.encode('utf-8'))

    def manage_join(self, message, active_client):
        """Adds a client to a chat room
        Creates a chat room if the one in question doesnt exist
        Increments the global room reference"""
        l.info(l_pre + 'Managing join for client')
        chatroom_name, client_name = parse_join(message)
        active_client.set_name(client_name)
        if(chatroom_name == None):
            print("Incomplete join call")
            return 
        if not(chatroom_name in self.active_chatrooms):
            self.active_chatrooms[chatroom_name] = chatroom(self.current_room_reference, chatroom_name)
            self.current_room_reference += 1
        self.active_chatrooms[chatroom_name].manage_client_join_and_response(active_client)
       
            
        
        

    def manage_chat(self, message, active_client):
        """parses message then sends it to the appropriate chat room"""
        l.info(l_pre + 'Sending chat to appropriate chatrooms')
        room_ref, join_id, client_name, message = parse_chat(message)
        temp_client = client(active_client.socket, active_client.address)
        temp_client.set_name(client_name)
        for room_name in self.active_chatrooms:
            if(self.active_chatrooms[room_name].room_reference == int(room_ref)):             
                self.active_chatrooms[room_name].send_message_to_connected_clients(message, temp_client)
                break

    def manage_leave(self, message, connection_socket):
        l.info(l_pre + 'Managing leave for client')
        print('managing leave for client')
        room_id, join_id, client_name = parse_leave(message)
        for room_name in self.active_chatrooms:
            if(self.active_chatrooms[room_name].room_reference == int(room_id)):
                self.active_chatrooms[room_name].remove_client_from_chatroom(client_name, join_id)    
                break

    def does_chatroom_exist(self, chatroom_name):
        for i, chatroom in enumerate(self.active_chatrooms):
            if chatroom[0].chatroom_name == chatroom_name:
                return i
        return -1
    
    
        #Function looking out for 'KILL_SERVICE' to end client socket
    def manage_command_line_input(self):
        """Function checking everything input on the command line and stopping the program if KILL_SERVICE is input """
        """Thread"""
        l.info(l_pre + 'Thread set up to manage command line info')
       '''  while 1:
            command = input()
            if command == "KILL_SERVICE":
                self.server_socket.close()
                os._exit(1)
                return
            elif command == "display":
                
                for chatroom_name in self.active_chatrooms:
                    connected_clients = self.active_chatrooms[chatroom_name].connected_clients
                    print(chatroom_name, ' has the following connected clients: ')
                    for client_name in connected_clients:
                        print(client_name, ' ') '''
                

ss = chat_server()  