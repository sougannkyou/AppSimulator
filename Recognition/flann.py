from pprint import pprint
import numpy as np
from datetime import datetime
import cv2
from matplotlib import pyplot as plt

cnt = 0
queryImage = cv2.imread('./images/kuaishou/share.png', 0)
trainingImage = cv2.imread('./images/kuaishou/bg1.png', 0)
# trainingImage = cv2.imread('./images/kuaishou/bb.jpg', 0)

start = datetime.now()

# create SIFT and detect/compute
sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(queryImage, None)
kp2, des2 = sift.detectAndCompute(trainingImage, None)

# FLANN matcher parameters
# FLANN_INDEX_KDTREE = 0
indexParams = dict(algorithm=0, trees=5)
searchParams = dict(checks=50)  # or pass empty dictionary

flann = cv2.FlannBasedMatcher(indexParams, searchParams)

matches = flann.knnMatch(des1, des2, k=2)

end = datetime.now()
print('times:', (end - start).microseconds)  # times: 105746

# prepare an empty mask to draw good matches
matchesMask = [[0, 0] for i in range(len(matches))]

for i, (m, n) in enumerate(matches):
    if m.distance < 0.7 * n.distance:
        matchesMask[i] = [1, 0]
        cnt += 1

pprint(matchesMask)

drawParams = dict(matchColor=(0, 255, 0),
                  singlePointColor=(255, 0, 0),
                  matchesMask=matchesMask,
                  flags=0)

pprint(drawParams)

resultImage = cv2.drawMatchesKnn(queryImage, kp1, trainingImage, kp2, matches, None, **drawParams)

plt.imshow(resultImage, ), plt.show()

cv2.drawKeypoints(queryImage, kp1, queryImage, (0, 255, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imwrite('temp.jpg', queryImage)

print(cnt > 0, cnt)
