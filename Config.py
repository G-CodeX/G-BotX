TOKEN = ""
LOG_PATH = ""
GUILD = 
STATUS_CHANNEL = 
VOICE = 
ACHIVEMENT = 
LEVEL_UP = 
HOSTNAME = ""    #Database Hostname
USERNAME = ""         #Database Username
PASSWORD = ""             #Database Password. Leave it empty("") if you didn't set any password
DATABASE = ""      #Database Name

#Functions
from mysql import connector as sql 
import time


def PrintEx(string: str):
    # TimeStamp
    time_ = time.localtime()
    timestamp = f"[{time_.tm_hour}:{time_.tm_min}:{time_.tm_sec}]       "
    print(f"{timestamp}{string}")
    return True

def write_log(log: str):
    # TimeStamp
    time_ = time.localtime()
    timestamp = f"[{time_.tm_hour}:{time_.tm_min}:{time_.tm_sec}]       "
    """
    Log function. You can print and write any log in bot.log
    Ex: write_log("Bot Activated.") {First it write "Bot Activated" in the bot.log then it will print "Bot Activated" in the consol}
    """
    try: # {try:, except:} this is a normal error handeling function
        with open(LOG_PATH, "a+t") as lw: # with function with grab the open module and access the bot.log
            lw.write(f"{timestamp}{log}\n")
            return 
    except Exception as e: # Exception contain the error and "as e" means it's defined by "e"
        raise print(f"{timestamp}{e}")
    
# Mysql Function
#Database Info
databaseinfo = {'user': USERNAME, 'password': PASSWORD, 'host': HOSTNAME, 'database': DATABASE, 'raise_on_warnings': True}


def ConnectToDatabase():
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        PrintEx("MySQL Connection Created Successfully")
    except Exception as e:
        PrintEx(f"Could not connect to MySQL DataBase. Exitting...")
        write_log(e)
        exit()

def sql_query(query):
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        cursor.execute(query)
        knowledgebase.commit()
        write_log(f"'{query}' this query is executed.")
        return 1
    except Exception as e:
        write_log(f"'{query}' isn't executed fully beacuse '{e}'")
        return 0

def GetSqlResult(query):
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        write_log(f"G-CodeX got the query result of '{query}'")
        return result
    except Exception as e:
        return write_log(f"G-CodeX can't execute '{query}' this query becasue: {e}")

def GetUserSerial(user_id: int):
    query = GetSqlResult(f"SELECT * FROM users WHERE user_id = {user_id}")
    if not query:
        return 'NULL'
    for i in query:
        serial = i[0]
    return serial
