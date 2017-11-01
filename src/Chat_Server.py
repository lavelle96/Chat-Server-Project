import threading
from socket import*
import sys
import os
from Chatroom import chatroom
from Message_Parser import parse_join, parse_chat
import logging as l
l_pre = 'CHAT_SERVER.PY: '

class chat_server():
    
    def __init__(self):
        """Set up thread to accept connections"""
        l.basicConfig(filename='Server.log',level=l.DEBUG)
        self.threads = []
        #active_chatrooms structure: ([Chatroom object, room reference])
        self.active_chatrooms = []
        self.current_room_reference = 0
        self.server_port = 10006
        self.server_socket = socket(AF_INET,SOCK_STREAM)
        self.server_socket.bind(('',self.server_port))
        self.server_socket.listen(1)
        print('The server is ready to receive')
        
        #Setup thread looking for command to quit program
        
        command_control_thread = threading.Thread(target=self.manage_command_line_input, args = (self.server_socket,))
        self.threads.append(command_control_thread)
        command_control_thread.start()
    
        while 1:
        #Accept connections from clients and start a new thread handling each new connection
            connection_socket, addr = self.server_socket.accept()
            
            new_connection_thread = threading.Thread(target = self.manage_connection_thread, args = (connection_socket, addr, self.server_socket,))
            self.threads.append(new_connection_thread)
            new_connection_thread.start()
            
        connection_socket.close()



    def manage_connection_thread(self, connection_socket, addr, server_socket):
        """Function invoked by new threads managing new connections"""
        l.info(l_pre + 'Managing new connection on new thread')
        while 1:
            received_data = connection_socket.recv(1024)

            #Close socket connection with client if their side is down
            if not received_data:
                print("Closing thread due to lack of data received")
                break
            
            message = received_data.decode()
            print(message)
            if(message == 'HELO text\n'):
                self.send_helo_response(connection_socket, server_socket)
            else:
                message_split = message.split()
                if(message_split[0] == 'JOIN_CHATROOM:'):
                   self.manage_join(message, connection_socket)
                elif(message_split[0] == 'CHAT:'):
                   self.manage_chat(message, connection_socket)
                    
        
        connection_socket.close()
        
    #Function looking out for 'KILL_SERVICE' to end client socket
    def manage_command_line_input(self, server_socket):
        """Function checking everything input on the command line and stopping the program if KILL_SERVICE is input """
        """Thread"""
        l.info(l_pre + 'Thread set up to manage command line info')
        while 1:
            command = input()
            if command == "KILL_SERVICE":
                server_socket.close()
                os._exit(1)
                return
            elif command == "display":
                #self.chatroom_lock.acquire()
                
                for chatroom in self.active_chatrooms:
                    connected_clients = chatroom[0].connected_clients
                    
                    print(chatroom[0].chatroom_name + " is size: " + str(len(connected_clients)) + " and has the following members:" ) 
                    for client in connected_clients:
                        print(client[0] + " ")
                    print('\n')
                #self.chatroom_lock.release() 

                
#----------------------FUNCTIONS TO MANAGE CLIENT CALLS----------------------

    def send_helo_response(self, connection_socket, server_socket):
        """Function called when the input is helo"""
        """Sends a message back to connected client"""
        ip_address = server_socket.getsockname()[0]
        port_number = server_socket.getsockname()[1]
        respond_with = ["HELO text\nIP:", str(ip_address), '\nPort:', str(port_number), '\nStudentID:14334496\n']
        message_to_send = " ".join([str(x) for x in respond_with])
        connection_socket.send(message_to_send.encode('utf-8'))

    def manage_join(self, message, connection_socket):
        """Adds a client to a chat room
        Creates a chat room if the one in question doesnt exist
        Increments the global room reference"""
        l.info(l_pre + 'Managing join for client')
        chatroom_name, client_name = parse_join(message)
        if(chatroom_name == None):
            print("Incomplete join call")
            return 
        chatroom_index = self.does_chatroom_exist(chatroom_name)
        #self.chatroom_lock.acquire()
        if(chatroom_index == -1):
            l.info(l_pre + 'Creating new chatroom')
            
            new_chatroom = chatroom(self.current_room_reference, chatroom_name)
            new_chatroom.manage_client_join_and_response(connection_socket, client_name)
            self.active_chatrooms.append([new_chatroom, self.current_room_reference])
            self.current_room_reference = self.current_room_reference + 1
        else:
            self.active_chatrooms[chatroom_index][0].manage_client_join_and_response(connection_socket, client_name)

    def manage_chat(self, message, connection_socket):
        """parses message then sends it to the appropriate chat room"""
        l.info(l_pre + 'Sending chat to appropriate chatrooms')
        room_ref, join_id, client_name, message = parse_chat(message)
        
        for chatroom in self.active_chatrooms:
            if chatroom[1] == int(room_ref):             
                chatroom[0].send_message_to_connected_clients(message, client_name, join_id)
                break

    def does_chatroom_exist(self, chatroom_name):
        for i, chatroom in enumerate(self.active_chatrooms):
            if chatroom[0].chatroom_name == chatroom_name:
                return i
        return -1
        

ss = chat_server()  