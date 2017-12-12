# Chat-Server-Project
A chat server using socket programming implemented in python.

## Run
To run the project, simply run the start.sh program:
- ./start.sh

## Implementation
- *Chatroom object* keeps track of which clients are in which chatroom, allocates a unique thread for each individual client (or each client socket connection) and handles joining and leaving of clients. All client interaction comes through the chat server object.
- *Chat server object* keeps track of which chatrooms are active and allows clients to connect to the chat server and from there join chatrooms
- *Locks* are used to make sure the data shared by the clients and chat server isnt corrupted, the Lock object from the threading class was used to implement this securely.

## Results
-The program obtained full marks when tested against the test server in TCD, passing every test available.
