

def join_response(chatroom_name, server_ip, port, room_ref, join_id):
    """Takes in strings and returns response string"""
    return "JOINED_CHATROOM: " + chatroom_name + "\nSERVER_IP: " + server_ip + "\nPORT: " + port + "\nROOM_REF: " + room_ref + "\nJOIN_ID: " + join_id + "\n"

def helo_response(text, ip, port, student_number):
    return  "HELO " + text + "\nIP: " + ip + '\nPort: ' + port + '\nStudentID: ' + student_number + '\n'

def leave_response(room_ref, join_id):
    return "LEFT_CHATROOM: " + str(room_ref) + '\nJOIN_ID: ' + str(join_id) + '\n'  
		  