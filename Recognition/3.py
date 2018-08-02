import cv2
import aircv as ac

# img_obj = ac.imread("douyin/share.png")
# img_bg = ac.imread("douyin/bg5.jpg")

# img_obj = ac.imread("images/huoshan/share.png")
# img_bg = ac.imread("images/huoshan/bg2.png")

img_obj = ac.imread("dianping_dafen.png")
img_bg = ac.imread("dianping_ng.png")


def debug(x, y):
    cv2.circle(img=img_bg, center=(int(x), int(y)), radius=30, color=(0, 0, 255), thickness=1)
    cv2.putText(img=img_bg, text='click', org=(int(x) - 40, int(y) + 10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=1)
    cv2.startWindowThread()
    cv2.imshow('Debugger', img_bg)
    cv2.waitKey(3 * 1000)
    cv2.destroyAllWindows()
    cv2.waitKey(100)


def test():
    pos = ac.find_template(img_bg, img_obj, threshold=0.7)
    print(pos)
    ret = ac.find_all_template(img_bg, img_obj, threshold=0.7)
    print(ret)
    return pos


if __name__ == '__main__':
    ret = test()
    (x, y) = ret['result']
    debug(x, y)
    print(cv2.getBuildInformation())
