#coding:GBK

import os,sys,inspect
import time
import telnetlib

def telnet_connect(host, port):
    try_max_times = 3
    conn = None
    while(try_max_times):
        try:
            conn = telnetlib.Telnet(host, port)
            print ("success telnet to ip : %s ,port : %s"%(host, port))
            break
        except Exception as e:
            print ("failed telnet to ip : %s ,port : %s ,reason : %s"%(host, port, e))
            
        try_max_times -= 1
        
    return conn
    
def telnet_close(conn):
    conn.close()
    
def telnet_write(conn, write_data):
    conn.write(write_data + '\n')
    
    
def telnet_read(conn,timeOut=10,intelligentWait=10,forwardFlag="#"):
    end_time = time.time() + timeOut
    waitCounter = -1
    recvData = ''
    try:
        while(True):
            data = conn.read_very_eager()
            if data:
                recvData += data
                if forwardFlag != '' and data.find(forwardFlag) != -1:
                    break
                waitCounter = intelligentWait
            else:
                if intelligentWait >=0 and waitCounter != -1:
                    if waitCounter > 0 :
                    waitCounter -= 1
                    time.sleep(0.1)
                else:
                    break
            if time.time() > end_time:
                break
    except Exception as reason:
        print ("read telnet info failed , error : %s"%reason)
        
        
def telnet_login(conn, user_flag, user, passwd_flag, passwd):
    telnet_read(conn,forwardFlag = user_flag)
    telnet_write(conn, user)
    telnet_read(conn,forwardFlag = passwd_flag)
    telnet_write(conn, passwd)  
    telnet_read(conn,forwardFlag = passwd_flag)
    data = telnet_read(conn, forwardFlag = '#')
    print ("data is : %s"%data)
    
    return conn
            