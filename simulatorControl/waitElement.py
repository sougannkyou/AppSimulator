import cv2
import aircv as ac

from PIL import ImageGrab

bbox = (760, 0, 1160, 1080)
im = ImageGrab.grab(bbox)
im.save('as.png')


def detect_obj(img, pos, circle_radius, color, line_width):
    cv2.circle(img, pos, circle_radius, color, line_width)
    cv2.imshow('detect_obj', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # imsrc = ac.imread('images/bg.png')
    # imobj = ac.imread('images/share.png')
    imsrc = ac.imread('images/bg_copylink.png')
    imobj = ac.imread('images/copylink.png')

    # find the match position
    pos = ac.find_template(imsrc, imobj)
    x, y = pos['result']
    circle_center_pos = (int(x), int(y))
    print(circle_center_pos)
    circle_radius = 40
    color = (0, 255, 0)
    line_width = 2

    detect_obj(imsrc, circle_center_pos, circle_radius, color, line_width)
