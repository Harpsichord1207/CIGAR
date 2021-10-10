import cv2
import dlib
import pathlib
import time

work_dir = pathlib.Path(__file__).parent.parent.parent.joinpath('resources').joinpath('trains')
svm_file = work_dir.joinpath('detector.svm')
detector = dlib.simple_object_detector(str(svm_file))


def draw(_rectangles, _img):
    for _rectangle in _rectangles:
        left, right = _rectangle.left(), _rectangle.right()
        top, bottom = _rectangle.top(), _rectangle.bottom()
        cv2.rectangle(_img, (left, top), (right, bottom), (0, 255, 0), 3)
        cv2.putText(_img, "This is Python Logo!", (left, top), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)


cam = cv2.VideoCapture(0)

rectangles = []
time1 = time.time()
interval = 1  # 识别出来之后让提示框多停留1秒钟

while 1:
    time2 = time.time()
    ret_val, img = cam.read()
    if len(rectangles) == 0 or time2 - time1 > interval:
        # rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rectangles = detector(rgb_image)
        time1 = time2

    draw(rectangles, img)
    cv2.imshow('CIGAR', img)
    if cv2.waitKey(1) == 27:
        break  # esc to quit

cv2.destroyAllWindows()

if __name__ == '__main__':
    pass
