# Remote streaming live video with Flask
This an implementation on how to get a remote live video streaming connection between 2 different processes using websockets. The video image is captured through [OpenCV](https://opencv.org/) on one machine and video is served in another machine. This approach serves best the scenario where the Webserver is located in a different network than the machine that is producing the video streaming.

The streaming process can be summed into the following steps:
1. Capturing video image
2. For each frame, serialize the image
3. Flush the data to the Webserver listening socket
4. Deserialize the data into a jpeg image
5. Serve the result in the web page

The web framkework used for the webserver is [Flask](http://flask.pocoo.org/). For example purposes, we will be using laptop's webcam image straight away.

## Install
This example runs with Python. Also install the following Python dependencies (pip makes it dead simple):
* opencv-python
* flask

## Usage
1. Start the server and visit your browser at "http://&lt;address&gt;:&lt;port&gt;/video_feed"
2. Start your client
3. Check yourself on the server
  
## Credits
The approach on how to serve the video on a webpage is taken from [this blog](http://blog.miguelgrinberg.com/post/video-streaming-with-flask).

## License
Code and documentation released under the [MIT License](https://github.com/rena2damas/remote-opencv-streaming-live-video/blob/master/LICENSE)
