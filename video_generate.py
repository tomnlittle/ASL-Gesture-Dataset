import os
from datetime import datetime
import cv2
from load_data import DATA_MAPPING, NO_IMAGE_NAME
from segTools import *

SAVE_LOCATION = './video/' + datetime.now().strftime('%Y%m%d-%H%M%S') + '/'
IMAGE_TYPE = '.jpg'
SHIFT = 0

def read_frame(cap):
  _, frame = cap.read()

  return frame

if __name__ == '__main__':

  # create the dirs
  os.makedirs(SAVE_LOCATION)

  # open capture
  cap = cv2.VideoCapture(0)

  # establish frame width and height for video output
  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))

  # setup video
  fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
  cropW = 200
  cropH = 200
  recordCroppedIm = True
  if recordCroppedIm == True:
    frame_width = cropW
    frame_height = cropH

  video = cv2.VideoWriter(SAVE_LOCATION + 'video.avi', fourcc, 30.0, (frame_width, frame_height))

  # generate an object that has a number for each of the letters of the alphabet
  image_count = test_num = dict.fromkeys(DATA_MAPPING.values(), 0)

  shift_triggered = False

  #set up segmentation
  bgs = cv2.createBackgroundSubtractorMOG2(varThreshold=500, detectShadows=False)
  # max_val, min_val = getRange(cap, 400, 130, 5)
  lastPos = [-1,-1]

  while(True):
    frame = read_frame(cap)
    im = frame.copy()
    cropped, _,_ = cutSquare(im, 100, 200, 200,200) #segForTraining(frame, max_val, min_val, lastPos)
    cv2.imshow('Video', frame)
    cv2.imshow('Crop', cropped)

    k = cv2.waitKey(1)
    letter = NO_IMAGE_NAME

    if (k == SHIFT or k== 225):
      print('SHIFT TRIGGERED : NOW RECORDING')
      print('PRESS ESC TO FINISH')
      shift_triggered = True

    # if letter pressed
    if (k >= 97 and k <= 122):
      letter = (chr(k)).upper()

    filename = letter + str(image_count[letter])

    if shift_triggered:
      print("Recording")
      # cv2.imwrite(SAVE_LOCATION + filename + IMAGE_TYPE, cropped)
      video.write(frame)

    image_count[letter] += 1

    if k == 27:

        break

  video.release()
  cap.release()
  cv2.destroyAllWindows()
