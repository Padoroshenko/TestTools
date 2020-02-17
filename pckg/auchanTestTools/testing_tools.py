import pysftp
import os
import fnmatch
import shutil
import csv
from subprocess import Popen,PIPE
import stomp
import ssl
import pandas
ERROR_CODE=-1
def putToSFTP(host,port,remote,login,password,privateKey,mask,local):
    try:
        sftp = pysftp.Connection(host=host,port=port, username=login, password=password,private_key=privateKey)
    except Exception as ex:
        return ERROR_CODE,ex
    else:
        with sftp.cd(remote):  # temporarily cd to remote
            for file in os.listdir(local):
                if(fnmatch.fnmatch(file,mask)):
                    sftp.put(remotepath=remote+"/"+file,localpath=local+"/"+file)  # upload to remote
        return 0, None

def getFromSFTP(host,port,remote,login,password,privateKey,mask,local):
    try:
        sftp = pysftp.Connection(host=host,port=port, username=login, password=password,private_key=privateKey)
    except Exception as ex:
        return ERROR_CODE,ex
    else:
        for file in sftp.listdir(remote):
            if (fnmatch.fnmatch(file, mask)):
                sftp.get(remotepath=remote + "/" + file, localpath=local + "/" + file)
        return 0,None


def runTalendJob(scriptpath):
    if (shutil.which('java') is None): # check if java executable found in PATH
        print("Add path to java executable to PATH")
        return None
    my_env = os.environ.copy()
    p = Popen(scriptpath,env=my_env,stdout=PIPE,stderr=PIPE)
    stdout, stderr = p.communicate()
    if(stderr is b""):
        return 0,stdout.decode("utf-8"),None
    else:
        return ERROR_CODE, stdout.decode("utf-8"), stderr.decode("utf-8")

def getCellValueFromCSV(filepath,delim,row,col):
    with open(filepath, 'r', encoding='utf-8') as temp_f:
        data = csv.reader(temp_f,delimiter=delim)
        data = list(data)
        return str(data[row][col])

def sendFileToMQ(host,port,queue,user,password,filepath,headers,properties):
    with open(filepath, 'r', encoding='utf-8') as temp_f:
        body = temp_f.readlines()
        body = ''.join(content)
        sendMessageToMQ(host,port,queue,user,password,headers,properties,body)

def openMQConnection(host,port,user,password):
    conn = stomp.Connection(host_and_ports=[(host, port)])
    conn.set_ssl(ssl_version=ssl.PROTOCOL_TLS)
    conn.connect(login=user, passcode=password)
    return conn


def sendMessageToMQ(host,port,queue,user,password,headers,properties,body=""):
    conn = openMQConnection(host,str(port),user,password)
    conn.send(destination=queue, body=body,headers=headers,**properties)
    conn.disconnect()

#def readMQMessage(host,port,queue,user,password,local_body_file,local_header_file,local_property_file):



def getCellValueFromPivot(filepath,delim,row,col):
    largest_column_count = 0
    with open(filepath, 'r',encoding='utf-8') as temp_f:
        # Read the lines
        lines = temp_f.readlines()

        for l in lines:
            # Count the column count for the current line
            column_count = len(l.split(delim)) + 1

            # Set the new most column count
            largest_column_count = column_count if largest_column_count < column_count else largest_column_count

    temp_f.close()

    column_names = [i for i in range(0, largest_column_count)]

    # Read csv
    df = pandas.read_csv(filepath, header=None, delimiter=delim, names=column_names)
    return str(df[col][row])