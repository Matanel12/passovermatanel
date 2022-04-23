import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), msg (str)
    Returns: Nothing
    """
    string = chatlib.build_message(code,msg)
    string=string.encode()
    conn.send(string)


# Implement Code


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket.
    Prints debug info, then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    # Implement Code
    # ..
    data=conn.recv(10024).decode()
    cmd, msg = chatlib.parse_message(data)
    return cmd, msg


def connect():
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(msg):
    print(msg)
    exit()


def login(conn):
    while True:
        username = input("Please enter username: \n")
        password= input("please enter your password")
        build_and_send_message(conn,"LOGIN", str(username)+"#"+str(password))
        cmd, msg=recv_message_and_parse(conn)
        print(cmd,msg)
        if cmd=="LOGIN_OK":
            break

def build_send_recv_parse(conn,comand,data):
    build_and_send_message(conn,comand,data)
    cmd,msg=recv_message_and_parse(conn)
    return cmd,msg

def get_score(conn):
    cmd,msg=build_send_recv_parse(conn,"MY_SCORE","")
    print(msg)

def play_question(conn):
    try:
        cmd,msg=build_send_recv_parse(conn,"GET_QUESTION","")
        if cmd=="YOUR_QUESTION":
            msg=msg.split("#")
            print("your question is: \n"+ msg[1])
            answer=input("write the num of your answer \n 1 : "+msg[2] +"\n 2 : "+msg[3]+"\n 3 : "+msg[4]+"\n 4 : "+msg[5]+ "\n")
            id=msg[0]
            cmd2,msg2=build_send_recv_parse(conn,"SEND_ANSWER",id+"#"+answer)
            if cmd2=="CORRECT_ANSWER":
                print("you answer is correct")
            elif cmd2=="WRONG_ANSWER":
                print("you are wrong the correct answer is: "+msg2+ ":" + msg[int(msg2)+1])
            else:
                print ("error")
        elif cmd=="NO_QUESTIONS":
            print("you have  finished all the question")
        else:
            print(msg)
    except BaseException as err:
        print("There was an error")
        return None


def get_highscore(conn):
    cmd, msg = build_send_recv_parse(conn, "HIGHSCORE", "")
    if cmd=="ALL_SCORE":
        print(msg)
    else:
        print(msg)


def get_logged_users(conn):
    cmd, msg = build_send_recv_parse(conn, "LOGGED", "")
    if cmd=="LOGGED_ANSWER":
        print(msg)
    else:
        print(msg)






def logout(conn):
    build_and_send_message(conn, "LOGOUT", "")



def main():
    # Implement code
    pass


if __name__ == '__main__':
    main()
    socket = connect()
    while True:
        answer = input("write the thing you want to do from that list: \n L:login, A:get another question, B:see my score,C:get highscore, D:get logged users,  E:logout")
        if answer == "get another question" or answer == 'A':
            play_question(socket)
        if answer == "see my score" or answer == 'B':
            get_score(socket)
        if answer == "get highscore"or answer=='C':
            get_highscore(socket)
        if answer == "get loogged users"or answer=='D':
            get_logged_users(socket)
        if answer =="login"or answer=="L":
            login(socket)
        if answer == "logout"or answer=="E":
            logout(socket)
            break