# Remote streaming live video
This an implementation on how to get a remote live video streaming connection between 2 different processes using websockets. The video image is captured through OpenCV. This approach serves best the scenario where the Webserver is located in a different network than the machine that is producing the video streaming.

The streaming process can be summed into the following steps:
1. Capturing video image
2. For each frame, encode the image
3. Flush the data to the Webserver listening socket
4. Decode the data into the image
5. Serve the result in the web page
