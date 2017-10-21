import threading
from socket import*
import sys
import os
from Chatroom import chatroom
from Message_Parser import parse_join

threads = []
#active_chatrooms structure: ([Chatroom object, room reference])
active_chatrooms = []
current_room_reference = 0

def main():
    """Main Function of program"""
    server_port = 10006
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',server_port))
    server_socket.listen(1)
    print('The server is ready to receive')
    
    #Setup thread looking for command to quit program
    quit_Check_Thread = threading.Thread(target=manage_command_line_input, args = (server_socket,))
    threads.append
    quit_Check_Thread.start()
 
    while 1:
       #Accept connections from clients and start a new thread handling each new connection
        connection_socket, addr = server_socket.accept()
        
        new_connection_thread = threading.Thread(target = manage_connection_thread, args = (connection_socket, addr, server_socket,))
        threads.append(new_connection_thread)
        new_connection_thread.start()
        
    connection_socket.close()



def manage_connection_thread(connection_socket, addr, server_socket):
    """Function invoked by new threads managing new connections"""
    print("New Thread Established for new connection: ", connection_socket, addr)

    while 1:
        received_data = connection_socket.recv(1024)

        #Close socket connection with client if their side is down
        if not received_data:
            print("Closing thread due to lack of data received")
            break
        
        message = received_data.decode()
        print(message)
        if(message == 'HELO text\n'):
            send_helo_response(connection_socket, server_socket)
        else:
            message_split = message.split()
            if(message_split[0] == 'JOIN_CHATROOM:'):
                manage_join(message, connection_socket)
                
    
    connection_socket.close()
    
#Function looking out for 'KILL_SERVICE' to end client socket
def manage_command_line_input(server_socket):
    """Function checking everything input on the command line and stopping the program if KILL_SERVICE is input """
    """Warning: will have to be altered if the command line is needed for any other functionality"""
    """Thread"""
    while 1:
        command = input()
        if command == "KILL_SERVICE":
            server_socket.close()
            os._exit(1)
            return
        elif command == "display":
          global active_chatrooms
          for chatroom in active_chatrooms:
              print(chatroom[0].chatroom_name)  

def send_helo_response(connection_socket, server_socket):
    """Function called when the input is helo"""
    """Sends a message back to connected client"""
    ip_address = server_socket.getsockname()[0]
    port_number = server_socket.getsockname()[1]
    respond_with = ["HELO text\nIP:", str(ip_address), '\nPort:', str(port_number), '\nStudentID:14334496\n']
    message_to_send = " ".join([str(x) for x in respond_with])
    connection_socket.send(message_to_send.encode('utf-8'))

def manage_join(message, connection_socket):
    chatroom_name, client_name = parse_join(message)
    chatroom_index = does_chatroom_exist(chatroom_name)
    if(chatroom_index == -1):
        global current_room_reference
        global active_chatrooms
        new_chatroom = chatroom(current_room_reference, chatroom_name)
        new_chatroom.addClient(connection_socket, client_name)
        active_chatrooms.append([new_chatroom, current_room_reference])
        current_room_reference = current_room_reference + 1
    else:
        active_chatrooms[chatroom_index][0].addClient(connection_socket, client_name)
    #parse message
    #Create chatroom if necessary
    #Add socket to chat room
    #Send message back to client with confirmation

def does_chatroom_exist(chatroom_name):
    for i, chatroom in enumerate(active_chatrooms):
        if chatroom[0].chatroom_name == chatroom_name:
            return i
    return -1

main()  