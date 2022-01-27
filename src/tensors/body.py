import cv2
import mediapipe as mp
import time

pose = mp.solutions.pose.Pose()
mp_drawer = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
ts = 0

right_hand_points = {16, 18, 20, 22}
left_hand_points = {15, 17, 19, 21}

if __name__ == '__main__':

    while True:
        success, img = cap.read()
        if not success:
            continue
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pose_results = pose.process(imgRGB)
        if not pose_results:
            continue
        h, w, c = img.shape
        mp_drawer.draw_landmarks(img, pose_results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        current_points = set()
        for _id, lm in enumerate(pose_results.pose_landmarks.landmark):
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
            cv2.putText(img, str(_id), (cx+5, cy+5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            if lm.visibility >= 0.75 and (_id in right_hand_points or _id in left_hand_points):
                current_points.add(_id)

        if current_points & right_hand_points == right_hand_points:
            print('举起了右手！')
        if current_points & left_hand_points == left_hand_points:
            print('举起了左手！')

        c_ts = time.time()
        fps = 1 / (c_ts - ts)
        ts = c_ts
        cv2.putText(img, str(round(fps, 2)), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
