import cv2
import dlib
import pathlib


work_dir = pathlib.Path(__file__).parent.parent.parent.joinpath('resources').joinpath('trains')
xml_file = work_dir.joinpath('annotate.xml')
svm_file = work_dir.joinpath('detector.svm')
test_file = work_dir.joinpath('test.jpeg')


def annotate():
    print('暂时手动标注，生成xml文件')


def train(option_c=5):
    options = dlib.simple_object_detector_training_options()
    options.add_left_right_image_flips = False
    options.C = option_c
    options.num_threads = 4
    options.be_verbose = True

    dlib.train_simple_object_detector(str(xml_file), str(svm_file), options)


def test1():
    # 使用cv2展示结果
    detector = dlib.simple_object_detector(str(svm_file))
    # image = Image.open(str(test_file))
    # image_array = np.asarray(image)  # 使用PIL读取再用numpy转array这种方法颜色会反转，暂不知道为啥
    image_array = cv2.imread(str(test_file))
    faces = detector(image_array, 1)
    for face in faces:
        left = face.left()
        right = face.right()
        top = face.top()
        bottom = face.bottom()
        cv2.rectangle(image_array, (left, top), (right, bottom), (128, 255, 128), 3)
    cv2.namedWindow("CV2", cv2.WINDOW_NORMAL)
    cv2.imshow("CV2", image_array)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test2():
    # 使用dlib展示结果 TODO: install x11?
    detector = dlib.simple_object_detector(str(svm_file))
    win_det = dlib.image_window()
    win_det.set_image(detector)
    win = dlib.image_window()
    img = dlib.load_rgb_image(str(test_file))
    win.clear_overlay()
    win.set_image(img)
    win.add_overlay(detector(img))
    dlib.hit_enter_to_continue()


if __name__ == '__main__':
    # train(5)
    # time.sleep(1)
    test1()
    test2()
