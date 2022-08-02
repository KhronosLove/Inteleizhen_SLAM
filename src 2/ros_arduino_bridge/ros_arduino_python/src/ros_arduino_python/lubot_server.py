#!/usr/bin/env python3

from socket import *
from threading import Thread
import test_nav
nav = test_nav.NavTest()

Host ="10.0.0.65"
PORT = 1111
BUFSIZE = 4096
ADDR = (Host,PORT)

tcpServer = socket(AF_INET,SOCK_STREAM)
tcpServer.bind(ADDR)
tcpServer.listen(10)

while 1:
    print('waiting for connection...')
    tcpClient,addr = tcpServer.accept()
    print(addr)
    
    while 1:
        try:
            data = tcpClient.recv(BUFSIZE)
            print(data.decode())
            if not data:
                print('------')
                break;
        
            act = data.decode()
            if act=='1':
                print("start")
                t = Thread(target=nav.action)
                t.start()
                tcpClient.send("ok".encode())
            elif act=='2':
                print("stop")
                t = Thread(target=nav.shutdown)
                t.start()    
                tcpClient.send("ok".encode())
            elif act=='3':
                t = Thread(target=nav.platUp)
                t.start()         
                tcpClient.send("ok".encode())     
            elif act=='4':
                t = Thread(target=nav.platDown)
                t.start()         
                tcpClient.send("ok".encode())  
            elif act=='5':
                t = Thread(target=nav.armUp)
                t.start()         
                tcpClient.send("ok".encode())  
            elif act=='6':
                t = Thread(target=nav.armDown)
                t.start()         
                tcpClient.send("ok".encode())              
        except:
            break
        #buf = '[aaaa]' + data.decode()
        #tcpClient.send(buf.encode())

    tcpClient.close()
tcpServer.close()


