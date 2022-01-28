import cv2
import mediapipe

from models import Message
from utils import logger


class BodyDetect:

    right_hand_points = {14, 16, 18, 20, 22}
    left_hand_points = {13, 15, 17, 19, 21}
    hand_points = right_hand_points | left_hand_points
    visibility_prob = 0.65

    def __init__(self, queue):
        # assert isinstance(queue, Queue)
        self.queue = queue
        self.pose = mediapipe.solutions.pose.Pose()
        self.drawer = mediapipe.solutions.drawing_utils

    def _run(self):
        cap = cv2.VideoCapture(0)
        # start_ts = 0
        while 1:
            ok, img = cap.read()
            if not ok:
                raise RuntimeError('Failed to get image from camera!')
            pose_results = self.pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            if pose_results and pose_results.pose_landmarks:
                h, w, c = img.shape
                # mp_drawer.draw_landmarks(img, pose_results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
                current_points = set()
                for _id, lm in enumerate(pose_results.pose_landmarks.landmark):
                    # cv2.putText(img, str(_id), (int(lm.x * w) + 5, int(lm.y * h) + 5),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    if _id not in self.hand_points:
                        continue
                    if lm.visibility < self.visibility_prob:
                        continue
                    cv2.circle(img, (int(lm.x * w), int(lm.y * h)), 5, (255, 0, 0), cv2.FILLED)
                    current_points.add(_id)

                if current_points & self.right_hand_points == self.right_hand_points:
                    logger.critical('Detect Attack Action!')
                    attack_message = Message(action='ATTACK')
                    self.queue.put(attack_message)
                if current_points & self.left_hand_points == self.left_hand_points:
                    defend_message = Message(action='DEFEND')
                    self.queue.put(defend_message)

                if current_points:
                    logger.critical(f'Current Points: {current_points}')

            cv2.imshow("ActionCamera", img)
            cv2.waitKey(1)

    def run(self):
        try:
            self._run()
        except Exception:
            logger.error('Failed to run, Error is:', exc_info=True)
            raise
