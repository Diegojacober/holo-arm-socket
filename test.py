# Echo client program
import socket
import time
import math

HOST = "192.168.15.2" # The remote host
PORT = 30002 # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# msg = "set_digital_out(2,True)" + "\n"
# s.send (msg.encode())

# msg = "movej([-1.95, -1.58, 1.16, -1.15, -1.55, 1.18], a=1.0, v=0.1)" + "\n"
# msg = "movej([-1.95, -1.58, 1.16, -1.15, -1.55, 1.18], a=1.0, v=1.1, t=0, r=0)" + "\n"
PI = math.pi
base = -0.5*PI
shoulder = -0.5*PI
elbow = -0.5*PI
wrist_1 = -0.5*PI
wrist_2 = 0.0*PI
wrist_3 = 0.25*PI

msg = f"movej([{base}, {shoulder}, {elbow}, {wrist_1}, {wrist_2}, {wrist_3}], a=1.4, v=1.05, t=0, r=0)" + "\n"
s.send(msg.encode())
time.sleep(10)


# time.sleep(2)
# msg = "set_digital_out(2,True)" + "\n"
# s.send (msg.encode())

data = s.recv(1024)
#data = data.decode("utf-8")
data = str(data)

s.close()

#print ("Received", repr(data))
print ("Received", data)
