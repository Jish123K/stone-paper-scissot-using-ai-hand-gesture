import cv2

import numpy as np

class HandDetector:

    """

    Finds Hands using blob detection and contour analysis techniques.

    Exports the landmarks in pixel format. Adds extra functionalities like

    finding how many fingers are up or the distance between two fingers.

    Also provides bounding box info of the hand found.

    """

    def __init__(self, blob_size=300, blob_threshold=0.3, min_contour_area=1000):

        """

        :param blob_size: size of the blob to detect hands

        :param blob_threshold: threshold for the blob detector

        :param min_contour_area: minimum area of the contour to consider as a hand

        """

        self.blob_size = blob_size

        self.blob_threshold = blob_threshold

        self.min_contour_area = min_contour_area

        self.fingers = []

        self.lmList = []

    def findHands(self, img, draw=True):

        """

        Finds hands in a BGR image.

        :param img: Image to find the hands in.

        :param draw: Flag to draw the output on the image.

        :return: Image with or without drawings

        """

        # convert to grayscale

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # create a blob detector and detect blobs

        blob_params = cv2.SimpleBlobDetector_Params()

        blob_params.filterByArea = True

        blob_params.minArea = 500

        blob_params.maxArea = self.blob_size

        blob_params.filterByCircularity = True

        blob_params.minCircularity = 0.7

        blob_params.filterByConvexity = True

        blob_params.minConvexity = 0.7

        blob_params.filterByInertia = True

        blob_params.minInertiaRatio = 0.3

        detector = cv2.SimpleBlobDetector_create(blob_params)

        keypoints = detector.detect(gray)

        # find the hand with the largest contour

        hands = []

        for keypoint in keypoints:

            x, y = int(keypoint.pt[0]), int(keypoint.pt[1])

            hand = self._findHand(img, x, y)

            if hand is not None:

                hands.append(hand)

        if draw:

            for hand in hands:

                cv2.drawContours(img, [hand["contour"]], -1, (0, 255, 0), 2)

                cv2.rectangle(img, hand["bbox"][0], hand["bbox"][1], (255, 0, 255), 2)

        if draw:

            return hands, img

        else:

            return hands

    def fingersUp(self, myHand):

        """

        Finds how many fingers are open and returns in a list.

        Considers left and right hands separately

        :return: List of which fingers are up

        """

        myLmList = myHand["lmList"]

        fingers = []

        # Thumb

        if myLmList[4][1] < myLmList[3][1]:

            fingers.append(1)

        else:

            fingers.append(0)

        # 4 Fingers

        for id in range(1, 5):

            if myLmList[id * 4 + 1][2] < myLmList[id * 4 - 1][2]:

                fingers.append(1)

            else:

                fingers.append(

 return fingers
                  def distance(self, p1, p2):

"""

Calculates distance between two points

:param p1: Point 1

:param p2: Point 2

:return: Distance between two points

"""

x1, y1 = p1

x2, y2 = p2

return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def _findHand(self, img, x, y):

"""

 return fingers

Finds the hand from the keypoints detected by the blob detector

:param img: Image

:param x: x-coordinate of the keypoint

:param y: y-coordinate of the keypoint

:return: Hand dict containing contour, bounding box, and landmark list

"""

height, width, _ = img.shape

mask = np.zeros((height, width), dtype=np.uint8)
                   # draw a circle around the keypoint

 r = int(self.blob_size * self.blob_threshold)

 cv2.circle(mask, (x, y), r, (255, 255, 255), -1)

 # get the contour with the largest area

 contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

 contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

 for contour in contours:

     area = cv2.contourArea(contour)

     if area < self.min_contour_area:

         continue

     # calculate the bounding box of the contour

     x_min, y_min, w, h = cv2.boundingRect(contour)

     x_max, y_max = x_min + w, y_min + h

     # find the landmarks

     lmList = self._findLandmarks(contour)

     if lmList is None:

         continue

     return {

         "contour": contour,

         "bbox": ((x_min, y_min), (x_max, y_max)),

         "lmList": lmList

     }
                  def _findLandmarks(self, contour):
"""
Finds the landmarks of the hand from the contour using convexity defects
:param contour: Contour of the hand
:return: Landmark list
"""
hull = cv2.convexHull(contour)
if hull is None:
return None
                   defects = cv2.convexityDefects(contour, cv2.convexHull(contour, returnPoints=False))

 if defects is None:

     return None

 lmList = []

 for i in range(defects.shape[0]):

     s, e, f, d = defects[i][0]

     start = tuple(contour[s][0])

     end = tuple(contour[e][0])

     far = tuple(contour[f][0])

     angle = self._calculateAngle(start, far, end)

     if angle > np.pi / 2.5:

         continue

     lmList.append((start[0], start[1]))

     lmList.append((far[0], far[1]))

     lmList.append((end[0], end[1]))

 return lmList
                  def _calculateAngle(self, a, b, c):

    """

    Calculates the angle between three points

    :param a: Point A

    :param b: Point B

    :param c: Point C

    :return: Angle between points in radians

    """

    v1 = np.array([a[0] - b[0], a[1] - b[1]])

    v2 = np.array([c[0] - b[0], c[1] - b[1]])

    angle = np.arctan2(np.linalg.det([v1,v2]),np.dot(v1,v2))

    return angle
