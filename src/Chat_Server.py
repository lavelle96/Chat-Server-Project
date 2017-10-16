import threading
from socket import*


threads = []
def main():
    serverPort = 10006

    serverSocket = socket(AF_INET,SOCK_STREAM)
    
    serverSocket.bind(('',serverPort))
    
    serverSocket.listen(1)
    print('The server is ready to receive')
    
   
    quit_Check_Thread = threading.Thread(target=LookForQuit, args = (serverSocket,))
    threads.append
    quit_Check_Thread.start()
    print("Checkpoint 1")
    while 1:
        connectionSocket, addr = serverSocket.accept()
        print("Attempting to start new thread")
        newConnectionThread = threading.Thread(target = ManageJoiningThread, args = (connectionSocket, addr,))
        threads.append(newConnectionThread)
        newConnectionThread.start()
        # Data incoming on the socket
        #packet.header, packet.data =s.unpack(incoming) # 
        
        
    connectionSocket.close()

def LookForQuit(serverSocket):
    print("Thread started looking for end")
    while 1:
        command = input()
        if command == "KILL_SERVICE":
            print("If statement reached")
            serverSocket.close()
            return

def ManageJoiningThread(connectionSocket, addr):
    print("New Thread Established for new connection: ", connectionSocket, addr)

    
    print(connectionSocket.recv(1024))
main()