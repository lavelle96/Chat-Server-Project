
class chatroom:
    
    server_port = 10006
    server_ip = 0
    """([client_name, join_id, connection_socket])"""

    def __init__(self, room_reference, chatroom_name):
        self.room_reference = room_reference
        self.chatroom_name = chatroom_name
        self.connected_clients = []
        self.current_id = 0
   
    def addClient(self, connection_socket, client_name):
        """Adds client to current connected_clients array and sends a confirmaion message back to the client"""
        new_client = [client_name, self.current_id, connection_socket]
        print('client ' + client_name + ' added ' + ' to ' + self.chatroom_name)
        self.connected_clients.append(new_client)
        message_response = ["JOINED_CHATROOM:", self.chatroom_name, "\nSERVER_IP:", self.server_ip, "\nPORT", self.server_port, "\nROOM_REF:", self.room_reference, "\nJOIN_ID:", self.current_id, "\n"]
        message_to_send = " ".join([str(x) for x in message_response])
        connection_socket.send(message_to_send.encode('utf-8'))
        self.current_id = self.current_id+1
        self.send_message_to_connected_clients(client_name + "has joined the chatroom", "server", connection_socket)
    
    def send_message_to_connected_clients(self, message, client_name, connection_socket):
        """Sends given message to every connected client in the chat room"""
        message_with_new_line = message + '\n\n'
        message_array = ["CHAT:", self.room_reference, "\nCLIENT_NAME:", client_name, '\nMESSAGE:', message_with_new_line, '\n']
        message_to_send = " ".join([str(x) for x in message_array])
        for client in self.connected_clients:
            if client[2] != connection_socket:
                print("Sending to: " + client[0])
                connection_socket = client[2]
                connection_socket.send(message_to_send.encode('utf-8'))

    def is_client_in_chatroom(self, join_id, client_name):
        """Checks whether or not a given client is in the chat room"""
        for client in self.connected_clients:
            if join_id == client[1] and client_name == client[0]:
                return True

        return False