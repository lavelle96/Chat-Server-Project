
from socket import

serverName = 'localhost'
serverPort = 12003
clientSocket=socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))


while 1:
    
    #clientSocket.send('Whatever data you want to send to the socket')
    
    #'However you want to package data received from the socket' = clientSocket.recv(1024)
    

clientSocket.close()



    


   
