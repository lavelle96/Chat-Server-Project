import threading
from socket import*
import sys
import os

threads = []

def main():
    """Main Function of program"""
    server_port = 10006
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',server_port))
    server_socket.listen(1)
    print('The server is ready to receive')
    
    #Setup thread looking for command to quit program
    quit_Check_Thread = threading.Thread(target=look_for_quit, args = (server_socket,))
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
           
    
    connection_socket.close()
    
#Function looking out for 'KILL_SERVICE' to end client socket
def look_for_quit(server_socket):
    """Function checking everything input on the command line and stopping the program if KILL_SERVICE is input """
    """Warning: will have to be altered if the command line is needed for any other functionality"""
    """Thread"""
    while 1:
        command = input()
        if command == "KILL_SERVICE":
            server_socket.close()
            os._exit(1)
            return

def send_helo_response(connection_socket, server_socket):
    """Function called when the input is helo"""
    """Sends a message back to connected client"""
    ip_address = server_socket.getsockname()[0]
    port_number = server_socket.getsockname()[1]
    respond_with = ["HELO text\nIP:", str(ip_address), '\nPort:', str(port_number), '\nStudentID:14334496\n']
    message_to_send = " ".join([str(x) for x in respond_with])
    connection_socket.send(message_to_send.encode('utf-8'))


main()  