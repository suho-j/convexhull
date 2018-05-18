from collections import namedtuple
import matplotlib.pyplot as plt
import random
import cv2
import numpy as np
Point = namedtuple('Point', 'x y')


#class ConvexHull(object):
_points = []
_hull_points = []

def __init__(self):
    pass

def _add(point):
    _points.append(point)

def _get_orientation( origin, p1, p2):
    '''
    Returns the orientation of the Point p1 with regards to Point p2 using origin.
    Negative if p1 is clockwise of p2.
    :param p1:
    :param p2:
    :return: integer
    '''
    difference = (
        ((p2.x - origin.x) * (p1.y - origin.y))
        - ((p1.x - origin.x) * (p2.y - origin.y))
    )

    return difference

def compute_hull():
    '''
    Computes the points that make up the convex hull.
    :return:
    '''
    points = _points

    # get leftmost point
    start = points[0]
    min_x = start.x
    for p in points[1:]:
        if p.x < min_x:
            min_x = p.x
            start = p

    point = start
    _hull_points.append(start)

    far_point = None
    while far_point is not start:

        # get the first point (initial max) to use to compare with others
        p1 = None
        for p in points:
            if p is point:
                continue
            else:
                p1 = p
                break

        far_point = p1

        for p2 in points:
            # ensure we aren't comparing to self or pivot point
            if p2 is point or p2 is p1:
                continue
            else:
                direction = _get_orientation(point, far_point, p2)
                if direction > 0:
                    far_point = p2

        _hull_points.append(far_point)
        point = far_point

def get_hull_points():
    if _points and not _hull_points:
        compute_hull()

    return _hull_points

def display():
    # image width, height
    img_width = 640
    img_height = 480

    # draw all points & draw convexhull
    img1 = _draw_all_points(_points, img_height, img_width)
    img2 = _draw_hull_points(_hull_points, img_height, img_width)
    img3 = _draw_hull_points(_hull_points, img_height, img_width)
    img4 = _draw_all_points(_points, img_height, img_width)
    dstimage = create_image_multiple(img_height, img_width, 3, 2, 2)
    showMultiImage(dstimage, img1, img_height, img_width, 3, 0, 0)
    showMultiImage(dstimage, img2, img_height, img_width, 3, 0, 1)
    showMultiImage(dstimage, img3, img_height, img_width, 3, 1, 0)
    showMultiImage(dstimage, img4, img_height, img_width, 3, 1, 1)

    cv2.imshow('img', dstimage)

    cv2.waitKey()
    cv2.destroyAllWindows()

def _draw_all_points(_points, img_height, img_width) :
    # all points
    x = [p.x for p in _points]
    y = [p.y for p in _points]

    # Create black blank image
    img = create_image(img_height, img_width, 3)

    # all points
    for p in range(0, len(_points)):
        cv2.circle(img, (x[p] + 150, y[p] + 150), 1, (0, 0, 0), thickness=2, lineType=1, shift=0)
    return img

def _draw_hull_points(_hull_points, img_height, img_width):
    # hull points
    hx = [p.x for p in _hull_points]
    hy = [p.y for p in _hull_points]

    # Create black blank image
    img = create_image(img_height, img_width, 3)

    # Draw line  from the hull point to the hull point
    # x-y offset, +150
    for hp in range(0, len(_hull_points) - 1):
        img = cv2.line(img, (hx[hp] + 150, hy[hp] + 150), (hx[hp + 1] + 150, hy[hp + 1] + 150), (0, 0, 0), 2)

    # Get a contour
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thr = cv2.threshold(imgray, 127, 255, 0)
    _, contours, _ = cv2.findContours(thr, cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[1]
    # check a convexhull
    check = cv2.isContourConvex(cnt)
    if not check:
        cnt = cv2.convexHull(cnt)

    # contour area
    area = cv2.contourArea(cnt)
    # contour length
    perimeter = cv2.arcLength(cnt, True)

    cv2.drawContours(img, [cnt], 0, (0, 0, 255), 3)
    cv2.putText(img, "area: %d" % area, (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    cv2.putText(img, "perimeter: %f" % perimeter, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    return img

# 흰색 이미지를 생성
# h : 높이
# w : 넓이
# color : 색상
def create_image(h, w, d):
    image = np.zeros((h, w, d), np.uint8)
    color = tuple(reversed((255, 255, 255)))
    image[:] = color
    return image

# 흰색 이미지를 생성 단 배율로 더 크게
# hcount : 높이 배수(2: 세로로 2배)
# wcount : 넓이 배수 (2: 가로로 2배)
def create_image_multiple(h, w, d, hcount, wcount):
    image = np.zeros((h * hcount, w * wcount, d), np.uint8)
    color = tuple(reversed((255, 255, 255)))
    image[:] = color
    return image

# 통이미지 하나에 원하는 위치로 복사(표시)
# dst : create_image_multiple 함수에서 만든 통 이미지
# src : 복사할 이미지
# h : 높이
# w : 넓이
# color : 색상
# col : 행 위치(0부터 시작)
# row : 열 위치(0부터 시작)
def showMultiImage(dst, src, h, w, d, col, row):
    # 3 color
    if d == 3:
        dst[(col * h):(col * h) + h, (row * w):(row * w) + w] = src[0:h, 0:w]
    # 1 color
    elif d == 1:
        dst[(col * h):(col * h) + h, (row * w):(row * w) + w, 0] = src[0:h, 0:w]
        dst[(col * h):(col * h) + h, (row * w):(row * w) + w, 1] = src[0:h, 0:w]
        dst[(col * h):(col * h) + h, (row * w):(row * w) + w, 2] = src[0:h, 0:w]


def main():
    #ch = ConvexHull()
    for _ in range(50):
        _add(Point(random.randint(-100, 100), random.randint(-100, 100)))

    print("Points on hull:", get_hull_points())
    display()


if __name__ == '__main__':
    main()