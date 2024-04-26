import numpy as np
import sys
import cv2

PREVIEW = 0
BLUR = 1
FEATURES = 2
CANNY = 3

feature_params = dict(
    maxCorners=100,
    qualityLevel=0.2,
    minDistance=15,
    blockSize=9
)

s = 0
if len(sys.argv) > 1:
    s = int(sys.argv[1])

image_filter = PREVIEW
alive = True

win_name = 'Camera filter'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
result = None

source = cv2.VideoCapture(s)

while alive:
    ret, frame = source.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if image_filter == PREVIEW:
        result = frame
    elif image_filter == CANNY:
        result = cv2.Canny(frame, 145, 150)
    elif image_filter == BLUR:
        result = cv2.blur(frame, (15, 15))
    elif image_filter == FEATURES:
        result = frame
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(frame_gray, **feature_params)
        if corners is not None:
            corners = np.int0(corners)
            for corner in corners:
                x, y = corner.ravel()
                cv2.circle(result, (x, y), 10, (0, 255, 0), 1)


    cv2.imshow(win_name, result)

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27 or key == ord('Q'):
        alive = False
    elif key == ord('p') or key == ord('P'):
        image_filter = PREVIEW
    elif key == ord('b') or key == ord('B'):
        image_filter = BLUR
    elif key == ord('f') or key == ord('F'):
        image_filter = FEATURES
    elif key == ord('c') or key == ord('C'):
        image_filter = CANNY

source.release()
cv2.destroyAllWindows()