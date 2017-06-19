import cv2
import imutils

def number_of_contours(image_name):

    #Open image with opencv
    image = cv2.imread(image_name)
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])

    #pre processing
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    grayFilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(grayFilter, 30, 200)

    #find contours in the edged image
    _,cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    class ShapeDetector:
        def __init__(self):
            pass

        def detect(self, c):
            # initialize the shape name and approximate the contour
            shape = "unidentified"
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            return len(approx)

    numberOfShapes = 0
    for c in cnts:
        sd = ShapeDetector()
        shape = sd.detect(c)
        if (shape < 5) and (shape > 2):
             numberOfShapes += 1

    return numberOfShapes

print(number_of_contours("Lecture_6_Integration.pdf-p25-93.png"))