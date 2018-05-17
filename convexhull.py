from collections import namedtuple
import matplotlib.pyplot as plt
import random
import cv2
import numpy as np
Point = namedtuple('Point', 'x y')


class ConvexHull(object):
    _points = []
    _hull_points = []

    def __init__(self):
        pass

    def add(self, point):
        self._points.append(point)

    def _get_orientation(self, origin, p1, p2):
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

    def compute_hull(self):
        '''
        Computes the points that make up the convex hull.
        :return:
        '''
        points = self._points

        # get leftmost point
        start = points[0]
        min_x = start.x
        for p in points[1:]:
            if p.x < min_x:
                min_x = p.x
                start = p

        point = start
        self._hull_points.append(start)

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
                    direction = self._get_orientation(point, far_point, p2)
                    if direction > 0:
                        far_point = p2

            self._hull_points.append(far_point)
            point = far_point

    def get_hull_points(self):
        if self._points and not self._hull_points:
            self.compute_hull()

        return self._hull_points

    def create_blank(width, height, rgb_color=(255, 255, 255)):
        """Create new image(numpy array) filled with certain color in RGB"""
        # Create black blank image
        image = np.zeros((height, width, 3), np.uint8)

        # Since OpenCV uses BGR, convert the color first
        color = tuple(reversed(rgb_color))
        # Fill image with color
        image[:] = color

        return image

    def display(self):
        # all points
        x = [p.x for p in self._points]
        y = [p.y for p in self._points]
        #plt.plot(x, y, marker='D', linestyle='None')

        # Create black blank image
        img_width = 640
        img_height = 480
        img_color = (255, 255, 255)
        img = np.zeros((img_height, img_width, 3), np.uint8)
        # Since OpenCV uses BGR, convert the color first
        color = tuple(reversed(img_color))
        # Fill image with color
        img[:] = color

        # all points
        img2 = img.copy()
        for p in range(0, len(self._points)):
            cv2.circle(img2, (x[p]+150, y[p]+150), 1, (0, 0, 0), thickness=2, lineType=1, shift=0)

        # hull points
        hx = [p.x for p in self._hull_points]
        hy = [p.y for p in self._hull_points]
        plt.plot(hx, hy)
        plt.title('Convex Hull')

        #for hp in range(0, len(self._hull_points)):
            #cv2.circle(img, (hx[hp]+150,hy[hp]+150), 1, (0,0,0), thickness=2, lineType=1, shift=0)

        for hp in range(0, len(self._hull_points)-1):
                img = cv2.line(img, (hx[hp] + 150, hy[hp] + 150), (hx[hp+1] + 150, hy[hp+1] + 150), (0, 0, 0), 2)

        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thr = cv2.threshold(imgray, 127, 255, 0)
        _, contours, _ = cv2.findContours(thr, cv2.RETR_TREE,
                                          cv2.CHAIN_APPROX_SIMPLE)

        cnt = contours[1]
        #print('contour의 개수:', len(contours))
        cv2.drawContours(img, [cnt], 0, (0, 255, 0), 3)

        check = cv2.isContourConvex(cnt)
        if not check:
            hull = cv2.convexHull(cnt)
            cv2.drawContours(img, [hull], 0, (0, 0, 255), 3)
            cv2.imshow('convexhull', img)
            area = cv2.contourArea(hull)
            perimeter = cv2.arcLength(hull, True)
        else:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            cv2.imshow('contour', img)

        print('contour 면적:', area)
        print('contour 길이:', perimeter)

        plt.show()

        cv2.imshow('contour2', img2)
        cv2.waitKey()
        cv2.destroyAllWindows()



def main():
    ch = ConvexHull()
    for _ in range(50):
        ch.add(Point(random.randint(-100, 100), random.randint(-100, 100)))

    print("Points on hull:", ch.get_hull_points())
    ch.display()


if __name__ == '__main__':
    main()