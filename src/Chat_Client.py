
from socket import *
import threading
import os
def main():
    serverName = 'localhost'
    serverPort = 10006
    clientSocket=socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    print("Connected to socket")


    quit_Check_Thread = threading.Thread(target=read_out_socket_messages, args = (clientSocket,))
    
    quit_Check_Thread.start()
   
    while 1:

        
        client_message = input()
        if(client_message == 'close'):
            execute_quit(clientSocket)
        elif(client_message == 'helo'):
            send_helo(clientSocket, serverName, serverPort)

   
            
    clientSocket.close()

#Function looking out for 'close' to end client socket
def execute_quit(clientSocket):
    clientSocket.close()
    os._exit(1)
    return

def read_out_socket_messages(clientSocket):
    while 1:
        receivedData = clientSocket.recv(1024)
        if not receivedData:
            print("Closing client thread due to lack of data received")
            break
        print(receivedData.decode())
    
    clientSocket.close

def send_helo(clientSocket, serverName, serverPort):
    message = 'HELO text\n'
    clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))
main()
    


   
