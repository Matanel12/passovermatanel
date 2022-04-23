# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT"
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR"
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name and data field and creates a valid protocol message
    Returns: str, or None if error occured
    """
    if len(str(cmd))>CMD_FIELD_LENGTH:
        print(1)
        return None
    if(len(str(data))>MAX_DATA_LENGTH):
        print(2)
        return None
    string  = ""
    times=CMD_FIELD_LENGTH-len(cmd)
    length=len (data)
    size=len(str(length))
    length=""
    for i in range(LENGTH_FIELD_LENGTH-size):
        length+=" "
    length=length+str(len (data))

    for i in range(times):cmd=cmd+" "
    string = cmd+DELIMITER+str(length)+DELIMITER+data
    splited = split_msg(string, 3)
    string = join_msg(splited)

    # Implement code ...

    return string


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    mess=split_msg(data,3)
    cmd=mess[0]
    msg=mess[2]
    length=mess[1]
    if cmd==None or length==None or msg ==None:
        print(0)
        return None,None
    if len(cmd)!=CMD_FIELD_LENGTH:
        print(1)
        return None, None
    if len(msg)>MAX_DATA_LENGTH:
        print(2)
        return None, None
    if len(length)!=4:
        print(3)
        return None, None
    cmd = cmd.replace(" ", "")
    length=length.replace(" ", "")
    if length.isdigit()==False:
        return None, None
    if len(msg)!= int(length):

        return None, None

    return cmd, msg


def split_msg(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's delimiter (|) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    splited=msg.split("|")
    if len(splited)!=expected_fields:
        NewList=[None,None,None]
        return NewList
    else:
        return splited


# Implement code ...


def join_msg(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the delimiter.
    Returns: string that looks like cell1|cell2|cell3
    """
    string=""
    for i in msg_fields:
        if i == None:
            return None
        string=string +str(i)+DELIMITER
    string=string[0:-1]
    return string
# Implement code ...