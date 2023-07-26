import cv2
import numpy
import socket
import struct
import threading
import time # Jiaxi
from io import BytesIO


class Streamer(threading.Thread):

    def __init__(self, hostname, port):
        threading.Thread.__init__(self)

        self.hostname = hostname
        self.port = port
        self.running = False
        self.streaming = False
        self.jpeg = None

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        s.bind((self.hostname, self.port))
        print('Socket bind complete')

        payload_size = struct.calcsize("Ld")

        s.listen(10)
        print('Socket now listening')

        self.running = True

        while self.running:

            print('Start listening for connections...')

            conn, addr = s.accept()
            print("New connection accepted.")

            fps = 0
            last_received_second = int(time.time())
            while True:

                data = conn.recv(payload_size)

                if data:
                    # Read frame size
                    msg_size = struct.unpack("Ld", data)[0]

                    # Calculate Latency # Jiaxi
                    sent_time = struct.unpack("Ld", data)[1]
                    rece_time = time.time()
                    print("Latency: " + str(rece_time - sent_time))

                    # Calculate FPS # Jiaxi
                    curr_received_second = int(rece_time)
                    if curr_received_second != last_received_second:
                        print("FPS: " + str(fps))
                        last_received_second = curr_received_second
                        fps = 0
                    fps += 1

                    # Read the payload (the actual frame)
                    data = b''
                    while len(data) < msg_size:
                        missing_data = conn.recv(msg_size - len(data))
                        if missing_data:
                            data += missing_data
                        else:
                            # Connection interrupted
                            self.streaming = False
                            break

                    # Skip building frame since streaming ended
                    if self.jpeg is not None and not self.streaming:
                        continue

                    # Convert the byte array to a 'jpeg' format
                    memfile = BytesIO()
                    memfile.write(data)
                    memfile.seek(0)
                    frame = numpy.load(memfile)

                    ret, jpeg = cv2.imencode('.png', frame)

                    self.jpeg = jpeg


                    self.streaming = True
                else:
                    conn.close()
                    print('Closing connection...')
                    self.streaming = False
                    self.running = False
                    self.jpeg = None
                    break

        print('Exit thread.')

    def stop(self):
        self.running = False

    def get_jpeg(self):
        return self.jpeg.tobytes()
