import cv2
import dlib
import pathlib

work_dir = pathlib.Path(__file__).parent.parent.parent.joinpath('resources').joinpath('trains')
svm_file = work_dir.joinpath('detector.svm')

detector = dlib.simple_object_detector(str(svm_file))
cam = cv2.VideoCapture(0)
color_green = (0, 255, 0)
line_width = 3

counts = 0


while 1:
    ret_val, img = cam.read()
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    det_list = detector(rgb_image)
    height, width, _ = img.shape
    for det in det_list:
        left, right = det.left(), det.right()
        top, bottom = det.top(), det.bottom()
        cv2.rectangle(img, (left, top), (right, bottom), color_green, line_width)
        cv2.putText(img, "This is Python Logo!", (left, top), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow('CIGAR', img)
    if cv2.waitKey(1) == 27:
        break  # esc to quit
    counts += 1
    print(f'Counts: {counts}, Det: {det_list}')

cv2.destroyAllWindows()

if __name__ == '__main__':
    pass
