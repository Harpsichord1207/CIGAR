import cv2
import dlib
import numpy as np

from PIL import Image


if __name__ == '__main__':
    # TODO: 彩色转灰白可以提高识别率？
    detector = dlib.get_frontal_face_detector()
    win = dlib.image_window()
    image = Image.open(r'D:\Projects\Py\CIGAR\resouces\face1.jpg')
    image_nparray = np.asarray(image)
    faces = detector(image_nparray, 1)
    for face in faces:
        left = face.left()
        right = face.right()
        top = face.top()
        bottom = face.bottom()
        cv2.rectangle(image_nparray, (left, top), (right, bottom), (0, 255, 128), 1)
    cv2.namedWindow("FaceDetect", cv2.WINDOW_NORMAL)
    cv2.imshow("FaceDetect", image_nparray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
