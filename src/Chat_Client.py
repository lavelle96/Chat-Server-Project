
from socket import *
import threading
import os
def main():
    serverName = 'localhost'
    serverPort = 10006
    clientSocket=socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    print("Connected to socket")


    quit_Check_Thread = threading.Thread(target=LookForQuit, args = (clientSocket,))
    
    quit_Check_Thread.start()
   
    while 1:

        
        message = input("Message received by the main thread: ")
        print("About to send: ", message)
        bytes_Sent = clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))
        #
            #'However you want to package data received from the socket' = clientSocket.recv(1024)
        print(bytes_Sent, " bytes sent")
   
            
    clientSocket.close()

def LookForQuit(clientSocket):
    
    while 1:
        command = input("Message to be received by the other thread: ")
        if command == "close":
            clientSocket.close()
            os._exit(1)
            return

main()
    


   
