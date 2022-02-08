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
                current_points_pos = {}
                for _id, lm in enumerate(pose_results.pose_landmarks.landmark):
                    # cv2.putText(img, str(_id), (int(lm.x * w) + 5, int(lm.y * h) + 5),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    if _id not in self.hand_points:
                        continue
                    if lm.visibility < self.visibility_prob:
                        continue
                    cv2.circle(img, (int(lm.x * w), int(lm.y * h)), 5, (255, 0, 0), cv2.FILLED)
                    current_points.add(_id)
                    current_points_pos[_id] = (int(lm.x * w), int(lm.y * h))

                if current_points & self.right_hand_points == self.right_hand_points:
                    logger.critical('Detect Attack Action!')
                    attack_message = Message(action='ATTACK')
                    attack_message.mat_data = self.get_hand_area(self.right_hand_points, current_points_pos, img)
                    cv2.rectangle(img, current_points_pos[14], current_points_pos[20], (0, 128, 128), 3)
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

    @staticmethod
    def get_hand_area(points, pos_dict, mat):
        min_x = min_y = max_x = max_y = None
        for _id in points:
            x, y = pos_dict[_id]
            if min_x is None or min_x > x:
                min_x = x
            if min_y is None or min_y > y:
                min_y = y
            if max_x is None or max_x < x:
                max_x = x
            if max_y is None or max_y < y:
                max_y = y
        return mat[min_y-100:max_y+100, min_x-100:max_x+100]
