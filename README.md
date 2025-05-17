# Air Piano
[client](https://github.com/sleepyllie/air-piano/tree/client)\
[server](https://github.com/sleepyllie/air-piano/tree/server)

Air Piano is a virtual piano which allows the detection of notes via camera, using computer software to collect the data and translate it into sounds based on the position of a user's fingers.

## Dependencies:
- Python 3.13
- Webcam
- Jetson Nano
- Jetson Inference

## Setup:
1. Connect a webcam & Jetson Nano.
2. Connect the host to your computer.
3. In the terminal, connect the server using the command " python3 server.py "
4. In the terminal, connect the client using the command " python3 pose.py "
