import cv2
import numpy
import socket
import struct
import threading
from io import BytesIO


class Streamer(threading.Thread):

    def __init__(self, hostname, port):
        threading.Thread.__init__(self)

        self.hostname = hostname
        self.port = port
        self.connected = False
        self.jpeg = None
        self.running = False

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        s.bind((self.hostname, self.port))
        print('Socket bind complete')

        payload_size = struct.calcsize("L")

        s.listen(10)
        print('Socket now listening')

        self.running = True

        while self.running:

            conn, addr = s.accept()
            print("Connection accepted.")

            while True:

                data = conn.recv(payload_size)

                if data:
                    # Read frame size
                    msg_size = struct.unpack("L", data)[0]

                    # Read the payload (the actual frame)
                    data = b''
                    while len(data) < msg_size:
                        data += conn.recv(msg_size-len(data))

                    # Convert the byte array to a 'jpeg' format
                    memfile = BytesIO()
                    memfile.write(data)
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
        self.running = False

    def client_connected(self):
        return self.connected

    def get_jpeg(self):
        return self.jpeg.tobytes()
