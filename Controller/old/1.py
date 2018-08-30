# coding:utf-8
import os
import sys
from datetime import datetime

sys.path.append(os.getcwd())
from PIL import Image
import pytesseract


def test():
    start = datetime.now()
    image = Image.open('./2.png')
    code = pytesseract.image_to_string(image, lang='chi_sim')
    print('--------------------------------------------------------------------------\n')
    if code:
        print(code.replace('\n\n', '\n'))
    else:
        print('not found comment')
    print('--------------------------------------------------------------------------\n')
    end = datetime.now()
    print('ocr times:', (end - start).seconds, 's')


if __name__ == '__main__':
    test()
