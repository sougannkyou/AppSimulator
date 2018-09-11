import cv2
from datetime import datetime
from Controller.setting import *


class NewsTitleList(object):
    def __init__(self, font_size=18, region=(0, 0, 480, 800)):
        self._DEBUG = False
        self.LINE_WORD_MIN = 5  # 5个字
        self.window_flags = cv2.WINDOW_NORMAL  # WINDOW_AUTOSIZE | WINDOW_KEEPRATIO | WINDOW_GUI_EXPANDED
        self._SHOW_TOP_X = 60
        self._SHOW_TOP_Y = 10
        self._font_size = font_size
        self._spacing = font_size * 3  # 行距为3倍字宽
        self._region = region
        self._img_obj = None
        self._work_path = WORK_PATH

    def morphology(self, gray):
        # 二值化 x方向求梯度 GRADIENT
        sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
        ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

        # binary = cv2.GaussianBlur(binary, (7, 7), 0)
        if self._font_size == 15:
            binary = cv2.medianBlur(binary, 3)
        elif self._font_size == 18:
            binary = cv2.medianBlur(binary, 3)
            binary = cv2.medianBlur(binary, 1)
            binary = cv2.medianBlur(binary, 1)
        else:  # self._font_size = 24
            binary = cv2.medianBlur(binary, 3)
            binary = cv2.medianBlur(binary, 3)
            binary = cv2.medianBlur(binary, 3)

        # 用于膨胀腐蚀的扁平核函数
        if self._font_size == 15:
            erosion_element = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 7))
            dilation_element = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))
            # dilation2_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))
        elif self._font_size == 18:
            erosion_element = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 7))
            dilation_element = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))
            # dilation2_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))
        else:  # self._font_size == 24:
            erosion_element = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
            dilation_element = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))
            # dilation2_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))

        # 膨胀：模糊汉字内部结构
        dilation = cv2.dilate(binary, dilation_element, iterations=1)

        # 腐蚀：去掉外围细节，散点，竖直线（扁平核）等
        erosion = cv2.erode(dilation, erosion_element, iterations=1)

        # 开运算(MORPH_OPEN)：先腐蚀后膨胀的过程。开运算可以用来消除小黑点，在纤细点处分离物体、平滑较大物体的边界的
        #               同时并不明显改变其面积。
        # 闭运算(MORPH_CLOSE)：先膨胀后腐蚀的过程。闭运算可以用来排除小黑洞。
        open = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

        if self._DEBUG:
            cv2.namedWindow("binary", self.window_flags)
            cv2.resizeWindow("binary", 300, 500)
            cv2.imshow("binary", binary)
            cv2.moveWindow("binary", self._SHOW_TOP_X, self._SHOW_TOP_Y)
            cv2.imwrite(self._work_path + '\\Controller\\images\\temp\\binary.png', binary)

            cv2.namedWindow("dilation", self.window_flags)
            cv2.resizeWindow("dilation", 300, 500)
            cv2.imshow("dilation", dilation)
            cv2.moveWindow("dilation", 300 + self._SHOW_TOP_X, self._SHOW_TOP_Y)
            cv2.imwrite(self._work_path + '\\Controller\\images\\temp\\dilation.png', dilation)

            cv2.namedWindow("erosion", self.window_flags)
            cv2.resizeWindow("erosion", 300, 500)
            cv2.imshow("erosion", erosion)
            cv2.moveWindow("erosion", 600 + self._SHOW_TOP_X, self._SHOW_TOP_Y)
            cv2.imwrite(self._work_path + '\\Controller\\images\\temp\\erosion.png', erosion)

            cv2.namedWindow("open", self.window_flags)
            cv2.resizeWindow("open", 300, 500)
            cv2.imshow("open", open)
            cv2.moveWindow("open", 600 + self._SHOW_TOP_X, 520 + self._SHOW_TOP_Y)
            cv2.imwrite(self._work_path + '\\Controller\\images\\temp\\open.png', open)

            # cv2.namedWindow("dilation2", cv2.WINDOW_NORMAL)
            # cv2.imshow("dilation2", dilation2)
            # cv2.imwrite("dilation2.png", dilation2)

        # return erosion
        return open

    def find_text_region(self, img):
        '''
        查找和筛选文字区域
        '''
        print('--------------------------------------------')
        region = []
        # RETR_EXTERNAL：仅提取外轮廓；  CHAIN_APPROX_SIMPLE：压缩直线冗余减少内存存储
        image, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # 筛选掉面积太小的
            area = cv2.contourArea(contour)
            if area < self._font_size * self._font_size * self.LINE_WORD_MIN / 10:
                continue

            # # 近似多边形，包围的边
            # epsilon = 0.01 * cv2.arcLength(contour, True)
            # approx = cv2.approxPolyDP(contour, epsilon, True)
            # print('approx:', len(approx))
            # cv2.drawContours(img, [contour], 0, 255, -1)
            # cv2.imshow('img', img)

            # rect = cv2.minAreaRect(contour)  # 最小的包裹斜矩形（可能有方向）
            # box = cv2.boxPoints(rect)  # box 是四个点的坐标
            # box = np.int0(box)

            # top_y = box[2][1]
            # bottom_y = box[0][1]
            # top_x = box[0][0]
            # bottom_x = box[2][0]

            x, y, w, h = cv2.boundingRect(contour)  # 最小包裹正矩形
            top_x, top_y, bottom_x, bottom_y = x, y, x + w, y + h

            # 筛选掉：限定范围以外的
            (_top_x, _top_y, _bottom_x, _bottom_y) = self._region
            if top_x < _top_x or top_y < _top_y or bottom_x > _bottom_x or bottom_y > _bottom_y:
                continue

            # 筛选掉：靠近顶端的可能是wifi、4G和电池
            if top_y < 25:
                continue

            height = abs(bottom_y - top_y)
            width = abs(top_x - bottom_x)

            # 筛选掉：宽度小于字宽要求
            if width < self.LINE_WORD_MIN * self._font_size:
                continue

            # 筛选掉：瘦高，留下矮宽的
            if height > width:
                continue

            # 筛选掉：太矮的
            if height < self._font_size * 0.6:
                continue

            # 筛选掉：文字宽度不够的
            if height * self.LINE_WORD_MIN > width:
                continue

            print('({},{}) ({},{})'.format(top_x, top_y, bottom_x, bottom_y))
            region.append((top_x, top_y, bottom_x, bottom_y))
            # region.append(box)

        return region

    def to_vh_box(self, box):  # 转换为水平垂直矩形，对角线坐标
        return min(box[0][0], box[1][0], box[2][0], box[3][0]), min(box[0][1], box[1][1], box[2][1], box[3][1]), \
               max(box[0][0], box[1][0], box[2][0], box[3][0]), max(box[0][1], box[1][1], box[2][1], box[3][1])

    def find_paragraph(self, region, iterations=2):
        if iterations == 0:
            return region

        focus = []
        merged = []

        for i in range(len(region)):
            if i in merged:
                continue

            top_x1, top_y1, bottom_x1, bottom_y1 = region[i]

            for j in range(len(region)):
                if j in merged or j == i:
                    continue

                top_x2, top_y2, bottom_x2, bottom_y2 = region[j]

                # 小于行间距
                if abs((bottom_y1 + top_y1) / 2 - (bottom_y2 + top_y2) / 2) < self._spacing:
                    print('({},{}) ({},{})>>> merge <<<({},{}) ({},{})'.format(
                        top_x1, top_y1, bottom_x1, bottom_y1, top_x2, top_y2, bottom_x2, bottom_y2
                    ))
                    focus.append((
                        min(top_x1, top_x2), min(top_y1, top_y2), max(bottom_x1, bottom_x2), max(bottom_y1, bottom_y2)
                    ))
                    merged.append(i)
                    merged.append(j)

        for k in range(len(region)):
            if k not in merged:
                focus.append(region[k])

        if self._DEBUG:
            for f in focus:
                (top_x, top_y, bottom_x, bottom_y) = f
                cv2.rectangle(
                    self._img_obj, (top_x, top_y), (bottom_x, bottom_y),
                    (0, 0, 255) if iterations == 1 else (255, 0, 255) if iterations == 2 else (255, 255, 0), 2)

            cv2.namedWindow("paragraph", self.window_flags)
            cv2.resizeWindow("paragraph", 480, 800)
            cv2.imshow("paragraph", self._img_obj)
            cv2.moveWindow("paragraph", 1200 + self._SHOW_TOP_X, self._SHOW_TOP_Y)
            cv2.imwrite(self._work_path + '\\Controller\\images\\temp\\paragraph.png', self._img_obj)

        return self.find_paragraph(focus, iterations - 1)

    def find_title(self, image_path):
        self._img_obj = cv2.imread(image_path)
        gray = cv2.cvtColor(self._img_obj, cv2.COLOR_BGR2GRAY)
        dilation = self.morphology(gray)
        region = self.find_text_region(dilation)
        # 画轮廓（绿） (蓝,绿,红)
        for rect in region:
            # cv2.drawContours(self._img_obj, [box], 0, (0, 255, 0), 2) # box 是4点的坐标
            (top_x, top_y, bottom_x, bottom_y) = rect  # rect 是2点的坐标
            cv2.rectangle(self._img_obj, (top_x, top_y), (bottom_x, bottom_y), (0, 255, 0), 2)

        if self._DEBUG:
            cv2.namedWindow("contours", self.window_flags)
            cv2.resizeWindow("contours", 300, 500)
            cv2.imshow("contours", self._img_obj)
            cv2.moveWindow("contours", 900 + self._SHOW_TOP_X, self._SHOW_TOP_Y)
            cv2.imwrite(self._work_path + '\\Controller\\images\\temp\\contours.png', self._img_obj)

        print('--------------------------------------------')
        paragraphs = self.find_paragraph(region, iterations=3)

        if self._DEBUG:
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return paragraphs


if __name__ == '__main__':
    print('--------------------------------------------')
    print('OpenCV Ver:{}'.format(cv2.getVersionString()))

    # image_path = 'test_image/text_line/news{}.png'.format(14)  # qq bug 14 18 17
    # image_path = 'test_image/text_line/qq{}.png'.format(6)  # bug: 6 open运算后解决6
    # image_path = 'test_image/text_line/baidu{}.png'.format(2)  # bug: 6
    # image_path = 'test_image/text_line/shouhu{}.png'.format(4)
    # image_path = 'test_image/text_line/sina{}.png'.format(4)  # bug:4
    # image_path = 'test_image/text_line/163_{}.png'.format(6)  # bug: 6 7
    image_path = 'test_image/text_line/ifeng{}.png'.format(8)  # bug:3 7 8 font_size=15

    start = datetime.now()
    d = NewsTitleList(font_size=18)
    d._DEBUG = True
    d.find_title(image_path)
    end = datetime.now()
    print('spend times:{}'.format(end - start))
