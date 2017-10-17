import threading
from socket import*
import sys
import os
threads = []

programActive = True
def main():
    serverPort = 10006

    serverSocket = socket(AF_INET,SOCK_STREAM)
    
    serverSocket.bind(('',serverPort))
    
    serverSocket.listen(1)
    print('The server is ready to receive')
    
   
    quit_Check_Thread = threading.Thread(target=LookForQuit, args = (serverSocket,))
    threads.append
    quit_Check_Thread.start()
 
    while 1:
       
        connectionSocket, addr = serverSocket.accept()
        
        newConnectionThread = threading.Thread(target = ManageJoiningThread, args = (connectionSocket, addr,))
        threads.append(newConnectionThread)
        newConnectionThread.start()
        
    connectionSocket.close()



def ManageJoiningThread(connectionSocket, addr):
    print("New Thread Established for new connection: ", connectionSocket, addr)

    while 1:
        receivedData = connectionSocket.recv(1024)
        if not receivedData:
            print("Closing thread due to lack of data received")
            break
        print(receivedData.decode())
    
    connectionSocket.close
    
#Function looking out for 'KILL_SERVICE' to end client socket
def LookForQuit(serverSocket):
    print("Thread started looking for end")
    while 1:
        command = input()
        if command == "KILL_SERVICE":
            serverSocket.close()
           
            os._exit(1)
            return

main()