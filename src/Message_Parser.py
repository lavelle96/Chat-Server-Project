


def parse_join(message):
    split_message = message.split('\n')
    if(len(split_message) < 4):
        return None, None

    chatroom_name = split_message[0][15:]
    client_name = split_message[3][13:]
    return chatroom_name, client_name

def parse_leave(message):
    split_message = message.split('\n')
    chat_room = split_message[0].split(':')[1][1:]
    join_id = split_message[1].split(':')[1][1:]
    client_name = split_message[2].split(':')[1][1:]
    return chat_room, join_id, client_name

def parse_disconnect(message):
    split_message = message.split('\n')
    client_ip = split_message[0].split(':')[1][1:]
    client_port = split_message[1].split(':')[1][1:]
    client_name = split_message[2].split(':')[1][1:]
    return client_ip, client_port, client_name

def parse_chat(message):
    split_message = message.split('\n')
    chat_room = split_message[0][6:]
    join_id = split_message[1][9:]
    client_name = split_message[2][13:]
    message = split_message[3][9:]
    message += '\n\n'
    return chat_room, join_id, client_name, message


#Testing Functions
def join_test():
    test_message_parse_join = "JOIN_CHATROOM: [chatroom name]\nCLIENT_IP: [0]\nPORT: [0]\nCLIENT_NAME: [string Handle to identifier client user]\n"
    print(parse_join(test_message_parse_join)) 

def chat_test():
    test_message_parse_chat = 'CHAT: [ROOM_REF]\nJOIN_ID: [integer identifying client to server]\nCLIENT_NAME: [string identifying client user]\nMESSAGE: [string terminated with \n\n]\n'
    print(parse_chat(test_message_parse_chat))

def leave_test():
    test_message = 'LEAVE_CHATROOM: [ROOM_REF]\nJOIN_ID: [integer previously provided by server on join]\nCLIENT_NAME: [string Handle to identifier client user]\n'
    print(parse_leave(test_message))

#leave_test()