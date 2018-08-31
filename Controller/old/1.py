import sys
import os
import time
from datetime import datetime
import cv2
import aircv as ac
from pprint import pprint

sys.path.append(os.getcwd())

img_obj = ac.imread('C:\workspace\pyWorks\AppSimulator\Controller\images\lofter\share.png')
_capture_obj = ac.imread('C:\workspace\pyWorks\AppSimulator\Controller\images\\temp\\1.png')

pos_list = ac.find_all_template(_capture_obj, img_obj, threshold=0.7)
pprint(pos_list)
