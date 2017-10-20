
from socket import *
import threading
import os

#send helo :to get rseponse from server of server ip address, port and student number
#send close :to end the client abruptly
#send join [chatroom name] [client name] :to join chat room 
#send leave [room reference] [join id] [client name] :to leave chat room
#send disconnect [client name] :to disconnect from server
#send chat [room reference] [join id] [client name] [chat message] :to send chat message 

#room reference: integer that uniquely identifies chat room on server
#join id: integer previously provided by server on join
#client name: string handle to identify client user
#chat message: string terminated with '\n\n'

def main():
    """The main function called to run the program"""
    server_name = 'localhost'
    server_port = 10006
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    print("Connected to socket")


    read_in_from_socket_thread = threading.Thread(target=read_in_socket_messages, args=(client_socket,))
    read_in_from_socket_thread.start()
   
    while 1:
    #Reading in input from the command line    
        client_message = input()
        if(client_message == 'close'):
            execute_quit(client_socket)
        elif(client_message == 'helo'):
            send_helo(client_socket, server_name, server_port)
        else:
            words_in_message = client_message.split()
            if words_in_message[0] == 'join':
                if len(words_in_message) == 3:
                    chatroom_name = words_in_message[1]
                    client_name = words_in_message[2]
                    send_join_chatroom(client_socket, server_name, server_port, chatroom_name, client_name)

            elif words_in_message[0] == 'leave':
                if len(words_in_message) == 4:
                    room_ref = words_in_message[1]
                    join_id = words_in_message[2]
                    client_name = words_in_message[3]
                    send_leave_chatroom(client_socket, server_name, server_port, room_ref, join_id, client_name)

            elif words_in_message[0] == 'disconnect':
                if len(words_in_message) == 2:
                    client_name = words_in_message[1]
                    send_disconnect(client_socket, server_name, server_port, client_name)

            elif words_in_message[0] == 'chat':
                if len(words_in_message) == 5:
                    room_ref = words_in_message[1]
                    join_id = words_in_message[2]
                    client_name = words_in_message[3]
                    chat_message = words_in_message[4]
                    send_chat(client_socket, server_name, server_port, room_ref, join_id, client_name, chat_message)
    
    client_socket.close()


def execute_quit(client_socket):
    """Function invoked to close socket connection and end the program"""
    client_socket.close()
    os._exit(1)
    return

def read_in_socket_messages(client_socket):
    """Function dealing with data coming from the server on the client socket"""
    while 1:
        receivedData = client_socket.recv(1024)
        if not receivedData:
            print("Closing client thread due to lack of data received")
            break
        print(receivedData.decode())
    
    client_socket.close()

def send_helo(client_socket, server_name, server_port):
    """Function invoked to provide the right format of message for helo command"""
    message = 'HELO text\n'
    client_socket.sendto(message.encode('utf-8'), (server_name, server_port))

def send_join_chatroom(client_socket, server_name, server_port, chatroom_name, client_name):
    """Function invoked to provide the right format of message for join command"""
    message = ['JOIN_CHATROOM:', chatroom_name, '\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME:', client_name, '\n' ]
    message_to_send = " ".join([str(x) for x in message])
    client_socket.sendto(message_to_send.encode('utf-8'), (server_name, server_port))

def send_leave_chatroom(client_socket, server_name, server_port, room_ref, join_id, client_name):
    """Function invoked to provide the right format of message for leave command"""
    message = ['LEAVE_CHATROOM:', room_ref, '\nJOIN_ID:', join_id, '\nCLIENT_NAME:', client_name, '\n']
    message_to_send = " ".join([str(x) for x in message])
    client_socket.sendto(message_to_send.encode('utf-8'), (server_name, server_port))

def send_disconnect(client_socket, server_name, server_port, client_name):
    """Function invoked to provide the right format of message for disconnect command"""
    message = ['DISCONNECT: 0\nPORT: 0\nCLIENT_NAME:', client_name, '\n']
    message_to_send = " ".join([str(x) for x in message])
    client_socket.sendto(message_to_send.encode('utf-8'), (server_name, server_port))

def send_chat(client_socket, server_name, server_port, room_ref, join_id, client_name, chat_message):
    """Function invoked to provide the right format of message for chat command"""
    message = ['CHAT:', room_ref, '\nJOIN_ID:', join_id, '\nCLIENT_NAME:', client_name, '\nMESSAGE:', chat_message, '\n']
    message_to_send = " ".join([str(x) for x in message])
    client_socket.sendto(message_to_send.encode('utf-8'), (server_name, server_port))


main()
    


   
