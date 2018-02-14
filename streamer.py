import cv2
import threading
import socket
import pickle
import struct

class Streamer (threading.Thread):
  def __init__(self, hostname, port):
    threading.Thread.__init__(self)

    self.hostname = hostname
    self.port = port
    self.jpeg = None
    self.connected = False

    self.isRunning = True

  def run(self):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    s.bind((self.hostname, self.port))
    print 'Socket bind complete'

    data = ""
    payload_size = struct.calcsize("L")

    s.listen(10)
    print 'Socket now listening'

    conn, addr = s.accept()

    while self.isRunning:

      while len(data) < payload_size:
        data += conn.recv(4096)
      packed_msg_size = data[:payload_size]
      data = data[payload_size:]
      msg_size = struct.unpack("L", packed_msg_size)[0]

      while len(data) < msg_size:
        data += conn.recv(4096)
      frame_data = data[:msg_size]
      data = data[msg_size:]

      frame = pickle.loads(frame_data)
      ret, jpeg = cv2.imencode('.jpg', frame)
      self.jpeg = jpeg

      self.connected = True

    self.out.release()
    self.connected = False

  def stop(self):
    self.isRunning = False

  def client_connected(self):
    return self.connected

  def get_jpeg(self):
    return self.jpeg.tobytes()

  def __del__(self):
    self.out.release()