import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))
while True:
    ret,frame=cap.read()
    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("L", len(data))+data)