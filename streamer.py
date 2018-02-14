import cv2
import threading
import socket
import struct
import StringIO
import json
import numpy

class Streamer (threading.Thread):
  def __init__(self, hostname, port):
    threading.Thread.__init__(self)

    self.hostname = hostname
    self.port = port
    self.connected = False
    self.jpeg = None

  def run(self):

    self.isRunning = True

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    s.bind((self.hostname, self.port))
    print 'Socket bind complete'

    data = ""
    payload_size = struct.calcsize("L")

    s.listen(10)
    print 'Socket now listening'

    while self.isRunning:

      conn, addr = s.accept()

      while True:

        data = conn.recv(4096)

        if data:
          packed_msg_size = data[:payload_size]
          data = data[payload_size:]
          msg_size = struct.unpack("L", packed_msg_size)[0]

          while len(data) < msg_size:
            data += conn.recv(10000)

          frame_data = data[:msg_size]

          memfile = StringIO.StringIO()
          memfile.write(json.loads(frame_data).encode('latin-1'))
          memfile.seek(0)
          frame = numpy.load(memfile)

          ret, jpeg = cv2.imencode('.jpg', frame)
          self.jpeg = jpeg

          self.connected = True

        else:
          conn.close()
          self.connected = False
          break

    self.connected = False

  def stop(self):
    self.isRunning = False

  def client_connected(self):
    return self.connected

  def get_jpeg(self):
    return self.jpeg.tobytes()