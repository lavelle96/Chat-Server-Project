
from socket import *
def main():
    serverName = 'localhost'
    serverPort = 10006
    clientSocket=socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    print("Connected to socket")

   
        
    clientSocket.send(b'Whatever data you want to send to the socket')
    print("Data sent to: ", clientSocket.getsockname)
        #'However you want to package data received from the socket' = clientSocket.recv(1024)
        

    clientSocket.close()


main()
    


   
