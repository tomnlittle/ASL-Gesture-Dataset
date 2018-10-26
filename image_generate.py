import sys
import os
from datetime import datetime
import cv2
from load_data import DATA_MAPPING, NO_IMAGE_NAME
from segTools import *

IMAGE_TYPE = '.jpg'

def read_frame(cap):
  _, frame = cap.read()
  return frame

if __name__ == '__main__':

  name = sys.argv[2]

  if (len(sys.argv) != 3):
    sys.exit()

  SAVE_LOCATION = './images/' + name + '/'

  # create the dirs
  if not os.path.exists(SAVE_LOCATION):
    os.makedirs(SAVE_LOCATION)

  # open capture
  video_location = sys.argv[1]
  cap = cv2.VideoCapture(video_location)


  # get files in directory
  files = os.listdir(SAVE_LOCATION)

  image_count = dict.fromkeys(DATA_MAPPING.values(), 0)

  # if there are files in the directory we dont want to override them
  for i in os.listdir(SAVE_LOCATION):
    letter = i[0] # take the first letter
    image_count[letter] += 1

  while(True):
    frame = read_frame(cap)

    cv2.imshow('Image', frame)

    k = cv2.waitKey(0)

    # if letter pressed
    if (k >= 97 and k <= 122):
      letter = (chr(k)).upper()
      filename = letter + str(image_count[letter])
      image_count[letter] += 1
      cv2.imwrite(SAVE_LOCATION + filename + IMAGE_TYPE, frame)

    if k == 27:
        break

  cap.release()
  cv2.destroyAllWindows()
