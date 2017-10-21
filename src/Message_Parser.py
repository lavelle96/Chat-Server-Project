
def parse_join(message):
    split_message = message.split('\n')
    chatroom_name = split_message[0][15:]
    client_name = split_message[3][13:]
    return chatroom_name, client_name

'''test_message = "JOIN_CHATROOM: [chatroom name]\nCLIENT_IP: [0]\nPORT: [0]\nCLIENT_NAME: [string Handle to identifier client user]\n"
print(parse_join(test_message))'''