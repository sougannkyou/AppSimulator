# coding:utf-8
import os
import sys
from pprint import pprint

sys.path.append(os.getcwd())
from PIL import Image
import cv2
import numpy as np
import aircv as ac


def test():
    obj = "C:\workspace\pyWorks\AppSimulator\Controller\images\\temp\\test.png"
    border = "C:\workspace\pyWorks\AppSimulator\Controller\images\\temp\\border_128_128.png"
    page_line = "C:\workspace\pyWorks\AppSimulator\Controller\images\\temp\\page_line.png"
    img_obj = ac.imread(obj)
    img_page_line = ac.imread(page_line)
    img_border = ac.imread(border)
    # l = ac.find_all_template(img_obj, img_border, threshold=0.5)
    l = ac.find_all_template(img_obj, img_page_line, threshold=0.95)
    pprint(l)


if __name__ == '__main__':
    test()
