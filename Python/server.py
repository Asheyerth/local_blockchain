#SERVER
#https://stackoverflow.com/questions/65219786/how-to-run-a-server-in-python
import os
import socket

s = socket.socket()
host = socket.gethostname()
port = 8080
s.bind((host, port))
print("Server started at: ", host)
print(port)
s.listen(1)
conn,addr = s.accept()
print(addr, "connected")