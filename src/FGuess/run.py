import cv2
import pathlib

from handutil import HandDetector

detector = HandDetector(max_hands=1)

finger_images = []
for image_file in pathlib.Path(__file__).parent.parent.parent.joinpath('resources').joinpath('fingers').iterdir():
    finger_images.append(cv2.imread(str(image_file.resolve())))

# 指尖列表，分别代表大拇指、食指、中指、无名指和小指的指尖
tip_ids = [4, 8, 12, 16, 20]

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()

        if success:
            # 检测手势
            img = detector.find_hands(img, draw=True)
            # 获取手势数据
            lms_list = detector.find_positions(img)
            if len(lms_list) > 0:
                fingers = []
                for tid in tip_ids:
                    # 找到每个指尖的位置
                    x, y = lms_list[tid][1], lms_list[tid][2]
                    cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
                    # 如果是大拇指，如果大拇指指尖x位置大于大拇指第二关节的位置，则认为大拇指打开，否则认为大拇指关闭
                    if tid == 4:
                        if lms_list[tid][1] > lms_list[tid - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    # 如果是其他手指，如果这些手指的指尖的y位置大于第二关节的位置，则认为这个手指打开，否则认为这个手指关闭
                    else:
                        if lms_list[tid][2] < lms_list[tid - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                # fingers是这样一个列表，5个数据，0代表一个手指关闭，1代表一个手指打开
                # 判断有几个手指打开
                cnt = fingers.count(1)

                # 找到对应的手势图片并显示
                finger_img = finger_images[cnt]
                w, h, c = finger_img.shape
                img[0:w, 0:h] = finger_img
                cv2.rectangle(img, (200, 0), (300, 100), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(cnt), (200, 100), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 255))

            cv2.imshow('Image', img)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
