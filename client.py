import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import StringIO
import json

cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))

while(cap.isOpened()):
  ret,frame=cap.read()

  memfile = StringIO.StringIO()
  np.save(memfile, frame)
  memfile.seek(0)
  data = json.dumps(memfile.read().decode('latin-1'))

  clientsocket.sendall(struct.pack("L", len(data))+data)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()