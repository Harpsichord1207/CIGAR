import cv2

video = cv2.VideoCapture(r'C:\Users\liutao3\Desktop\超超最帅.mov')

while 1:
    ret_val, img = video.read()
    cv2.imshow('CIGAR', img)
    if cv2.waitKey(1) == 27:
        break  # esc to quit


if __name__ == '__main__':
    pass
