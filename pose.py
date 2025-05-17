#!/usr/bin/env python3
#
# Copyright (c) 2021, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
key_dictionary = {
                    (975, 265): "C",(895, 250) : "D", (800, 240) : "E", (725, 250) : "F", 
                    (640, 250) : "G", (560, 250) : "A", (460, 250) : "B", (370, 250) : "3C", 
                    (920, 450) : "C#", (840, 415) : "D#", (660, 410) : "F#", (570, 400) : "G#",
                   (495, 420) : "A#", (365, 430) : "3C#"
                }
import sys
from requests import post, get
import argparse

from jetson_inference import poseNet
from jetson_utils import videoSource, videoOutput, Log


LIMIT_X = 35
LIMIT_Y = 40

def within_range(pos):
    for key in key_dictionary:
        if int(pos[0]) in range(key[0]- LIMIT_X, key[0] + LIMIT_X):
            if int(pos[1]) in range(key[1] - LIMIT_Y, key[1] + LIMIT_Y):
                 print(key_dictionary[key])
                 return key_dictionary[key]
    return 


# parse the command line
parser = argparse.ArgumentParser(description="Run pose estimation DNN on a video/image stream.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=poseNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
#parser.add_argument("--network", type=str, default="resnet18-hand", help="pre-trained model to load (see below for options)")

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# load the pose estimation model
net = poseNet("resnet18-hand", "--network=resnet18-hand", 0.15)

# create video sources & outputs
input = videoSource("/dev/video0")

print("READY")

poses = []

def process():
    img = input.Capture()

    if img is None:
        return
    poses = net.Process(img)
    return poses


# process frames until EOS or the user exits
def get_notes(poses):
    buffer = []

    for pose in poses:
        #print(pose)
        
        # print(pose.Keypoints)
        # print('Links', pose.Links)

        kp = pose.Keypoints
        for key in kp:
             if key.ID in [5, 9, 13, 17, 21]:
                #print(key)
                print(within_range((key.x, key.y)))
                buffer.append(within_range((key.x, key.y)))
    return buffer

while True:
    poses = process()
    notes = get_notes(poses)
    notes = [note for note in notes if note != None]
    print(notes)
    if notes:  
        post("http://192.168.7.167:8000/store-note", data = {"notedata" : notes})
        print("storing note")
    get("http://192.168.7.167:8000/execute-buffer")