import cv2
import dlib
import numpy as np
import pathlib

from PIL import Image

face1_file = pathlib.Path(__file__).parent.parent.parent.joinpath('resources').joinpath('face1.jpg')


if __name__ == '__main__':
    # TODO: 彩色转灰白可以提高识别率？
    detector = dlib.get_frontal_face_detector()
    # win = dlib.image_window()
    image = Image.open(str(face1_file))
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
