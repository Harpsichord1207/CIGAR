import cv2
import dlib
import numpy as np
import pathlib

from PIL import Image


work_dir = pathlib.Path(__file__).parent.parent.parent.joinpath('resources').joinpath('doraemons')
xml_file = work_dir.joinpath('doraemons.xml')
svm_file = work_dir.joinpath('doraemons.svm')
test_file = work_dir.joinpath('test.jpg')


def annotate():
    print('暂时手动标注，生成xml文件')


def train():
    options = dlib.simple_object_detector_training_options()
    options.add_left_right_image_flips = True
    options.C = 5
    options.num_threads = 4
    options.be_verbose = True

    dlib.train_simple_object_detector(str(xml_file), str(svm_file), options)


def test():
    detector = dlib.simple_object_detector(str(svm_file))
    image = Image.open(str(test_file))
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


if __name__ == '__main__':
    # train()
    test()
