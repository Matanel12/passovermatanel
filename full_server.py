import socket
import select
import chatlib
import random
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later
open_client_sockets = []
messages_to_send = []

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"

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
    messages_to_send.append((conn,string))
    print("[SERVER] ", string)  # Debug print


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
    print("[CLIENT] ", data)  # Debug print
    return cmd, msg

def print_client_sockets():
    for i in logged_users:
        print(i+" \n")

# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    alldict={}
    counter=0
    questions =open("questions.txt",'r')
    q=questions.read()
    q=q.split("\n")
    help=["question","answers","correct"]
    for i in q:
        ans=[i.split("|")[0],[i.split("|")[1],i.split("|")[2],i.split("|")[3],i.split("|")[4]],i.split("|")[5]]
        dictionary = dict(zip(help, ans))
        alldict[counter]=dictionary
        counter+=1

    questions=alldict
    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    users = open("users.txt",'r')
    alldict = {}
    x=(users.read())
    x=x.split("\n")
    help = ["password", "score", "questions_asked"]
    for i in x:
        name=i.split("|")[0]
        ans = [i.split("|")[1], int(i.split("|")[2]), i.split("|")[3]]
        if len(ans[2])==0:
            ans[2] = []
        elif len(ans[2])==1:
            ans[2] = [ans[2]]
        else:
            helpl=ans[2].split(",")
            ans[2]=helpl
        dictionary = dict(zip(help, ans))
        alldict[name] = dictionary
    users=alldict
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print(f"SERVER IS UP ON PORT {SERVER_PORT}")
    server_socket.listen(10024)
    return server_socket




def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    ans=chatlib.build_message("ERROR", error_msg)
    messages_to_send.append((conn, ans.encode()))




def handle_getscore_message(conn, username):
    global users
    data=str(users[username]["score"])
    msg=chatlib.build_message("YOUR_SCORE",data)
    messages_to_send.append((conn,msg.encode()))
# Implement this in later chapters


def handle_logout_message(conn):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users
    if conn.getpeername()in logged_users:
        del logged_users[conn.getpeername()]
    for i in range(len(open_client_sockets)):
        if open_client_sockets[i]==conn:
            del open_client_sockets[i]





# Implement code ...


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users	 # To be used later
    cmd,msg=chatlib.parse_message(data)
    if cmd=="LOGIN":
        if ("#") in msg:
            msg=msg.split("#")
            if len(msg)==2:
                name=msg[0]
                password=msg[1]
                if name in users:
                    if password==users[name]["password"]:
                        if conn.getpeername() not in logged_users and name not in logged_users.values():
                            res = chatlib.build_message("LOGIN_OK", "")
                            logged_users[conn.getpeername()] = name
                        else:
                            res=chatlib.build_message("ERROR","you are already login")
                    else:
                        res=chatlib.build_message("ERROR","your password is incorrect")
                else:
                    res = chatlib.build_message("ERROR", "this username does not exist")
            else:
                res = chatlib.build_message("ERROR", "your structure is wrong")
        else:
            res = chatlib.build_message("ERROR", "your structure is wrong")
    else:res = chatlib.build_message("ERROR", "an error in the server command received  ")
    messages_to_send.append((conn,res.encode()))


def handle_high_score(conn):
    score_list=[]
    for i in users:
        current=(i,users[i]["score"])
        score_list.append(current)
    score_list.sort(key=lambda y: y[1], reverse=True)
    data=""
    for i in range(5):
        if i<len(score_list):
            data+= score_list[i][0] + " : "+str(score_list[i][1])+"\n"
    ans=chatlib.build_message("ALL_SCORE",data)
    messages_to_send.append((conn,ans.encode()))



# Implement code ...

def create_random_question(username):
    pl=[]
    for i in questions:
        if i not in users[username]["questions_asked"]:
            pl.append(i)
    if len(pl) ==0:
        return None
    else:
        amount=len(pl)
        num=random.randrange(amount)
        id= pl[num]
        q=questions[id]["question"]
        a=questions[id]["answers"]
        data=str(id)+"#"+q+"#"+str(a[0])+"#"+str(a[1])+"#"+str(a[2])+"#"+str(a[3])
        msg=chatlib.build_message("YOUR_QUESTION",data)
        users[username]["questions_asked"].append(id)
        return msg

def handle_answer_message(conn,username,data):
    if "#" in data:
        data=data.split("#")
        id = data[0]
        answer = data[1]
        if len(data)==2:
            true_answer = str(questions[int(id)]["correct"])
            if answer==true_answer:
                a=chatlib.build_message("CORRECT_ANSWER","")
                messages_to_send.append((conn,a.encode()))
                users[username]["score"]+=5
            else:
                a = chatlib.build_message("WRONG_ANSWER",true_answer)
                messages_to_send.append((conn, a.encode()))

        else:
            send_error(conn,"you added a #")
    else:send_error(conn,"you didnt write your answer")

def handle_question_message(conn,username):
    data = create_random_question(username)
    if data ==None:
        data=chatlib.build_message("NO_QUESTIONS", "")
    messages_to_send.append((conn,data.encode()))



def handle_loged_users(conn):
    data=""
    for i in logged_users:
        data+=logged_users[i]
    msg=chatlib.build_message("LOGGED_ANSWER",data)
    messages_to_send.append((conn,msg.encode()))



def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users	 # To be used later
    if cmd=="LOGIN":
        msg=chatlib.build_message(cmd,data)
        if conn.getpeername() not in logged_users:
            handle_login_message(conn,msg)
        else:
            res = chatlib.build_message("ERROR", "you are already login")
    elif conn.getpeername() in logged_users:
        if cmd=="MY_SCORE":
            handle_getscore_message(conn, logged_users[conn.getpeername()])
        elif cmd=="GET_QUESTION":
            handle_question_message(conn,logged_users[conn.getpeername()])
        elif cmd=="SEND_ANSWER":
            handle_answer_message(conn,logged_users[conn.getpeername()],data)
        elif cmd=="LOGOUT":
            handle_logout_message(conn)
            conn.close()
        elif cmd=="HIGHSCORE":
            handle_high_score(conn)
        elif cmd=="LOGGED":
            handle_loged_users(conn)
        elif cmd!="LOGIN":
            send_error(conn,"wrong command")
        else:
            send_error(conn, "you are not logedin")








# Implement code ...


def send_waiting_messages(wlist):
   for message in messages_to_send:
      current_socket, data = message
      if current_socket in wlist:
         current_socket.send(data)
         messages_to_send.remove(message)


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions
    global messages_to_send

    print("Welcome to Trivia Server!")


if __name__ == '__main__':
    main()
    questions=load_questions()
    users=load_user_database()
    server_socket=setup_socket()
    while True:
        try:
            rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
            for current_socket in rlist:
                if current_socket is server_socket:
                    (new_socket, address) = server_socket.accept()
                    print("new socket connected to server: ", new_socket.getpeername())
                    open_client_sockets.append(new_socket)
                else:
                    print('New data from client!')
                    cmd,msg=recv_message_and_parse(current_socket)
                    handle_client_message(current_socket,cmd,msg)
            send_waiting_messages(wlist)
        except ConnectionResetError :
            handle_logout_message(current_socket)
            current_socket.close()





