import queue

import cv2
import logging
import mediapipe as mp
import sys
import time
import pygame

from multiprocessing import Process, Queue


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s]: %(message)s'
)

logger = logging.getLogger(__name__)


class Message:

    def __init__(self, action, timestamp=None):
        self.timestamp = timestamp or time.time()
        self.action = action

    def __str__(self):
        return f'Message[{self.action}/{self.timestamp}]'


def run_game(message_queue):

    pygame.init()
    size = width, height = 800, 600

    screen = pygame.display.set_mode(size)
    hero_img = pygame.image.load(r'D:\Projects\Py\CIGAR\resources\game_outman.png').convert()
    hero_img = pygame.transform.scale(hero_img, (80, 120))

    monster_img = pygame.image.load(r'D:\Projects\Py\CIGAR\resources\game_monster.jpg').convert()
    monster_img = pygame.transform.scale(monster_img, (80, 120))

    is_attacking = 0

    logger.critical('PyGame init success, starting...')

    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # assert isinstance(message_queue, Queue)
        try:
            first_message = message_queue.get_nowait()
            assert isinstance(first_message, Message)
            if time.time() - first_message.timestamp >= 1:  # 延迟超过1s的就不要了
                logger.warning('Got Delayed Message, Will Ignore!')
                raise queue.Empty
        except queue.Empty:
            first_message = None

        if is_attacking == 0 and first_message is not None and first_message.action == 'ATTACK':
            logger.critical(f'Got Attack Message: {first_message}')
            screen.blit(hero_img, (10, 240))
            screen.blit(monster_img, (660, 240))
            pygame.draw.rect(screen, (17, 238, 238), (36, 270, 700, 20), 10)
            is_attacking += 1
        elif 0 < is_attacking <= 100:
            # logger.critical(f'Keep Attacking...')
            screen.blit(hero_img, (10, 240))
            screen.blit(monster_img, (660, 240))
            pygame.draw.rect(screen, (17, 238, 238), (36, 270, 700, 20), 10)
            is_attacking += 1
        else:
            screen.fill(color=(0, 0, 0))
            screen.blit(hero_img, (10, 240))
            screen.blit(monster_img, (660, 240))
            is_attacking = 0

        pygame.display.update()
        if first_message is not None:
            logger.critical(f'Finish Draw {first_message}')


def run_detect(message_queue):
    pose = mp.solutions.pose.Pose()
    mp_drawer = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    ts = 0

    right_hand_points = {14, 16, 18, 20, 22}
    left_hand_points = {13, 15, 17, 19, 21}
    while 1:
        success, img = cap.read()
        if not success:
            continue
        pose_results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if pose_results and pose_results.pose_landmarks:
            h, w, c = img.shape
            # mp_drawer.draw_landmarks(img, pose_results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
            current_points = set()
            for _id, lm in enumerate(pose_results.pose_landmarks.landmark):
                # cv2.putText(img, str(_id), (int(lm.x * w) + 5, int(lm.y * h) + 5),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                if _id not in (right_hand_points | left_hand_points):
                    continue
                if lm.visibility >= 0.65 and (_id in right_hand_points or _id in left_hand_points):
                    cv2.circle(img, (int(lm.x * w), int(lm.y * h)), 5, (255, 0, 0), cv2.FILLED)
                    current_points.add(_id)

            if current_points & right_hand_points == right_hand_points:
                logger.critical('Detect Attack Action!')
                attack_message = Message(action='ATTACK')
                message_queue.put(attack_message)
            if current_points & left_hand_points == left_hand_points:
                defend_message = Message(action='DEFEND')
                message_queue.put(defend_message)

            if current_points:
                logger.critical(f'Current Points: {current_points}')

        c_ts = time.time()
        fps = 1 / (c_ts - ts)
        ts = c_ts
        cv2.putText(img, str(round(fps, 2)), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("ActionCamera", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    global_message_queue = Queue()

    game_process = Process(target=run_game, args=(global_message_queue,))
    camera_process = Process(target=run_detect, args=(global_message_queue,))

    game_process.start()
    camera_process.start()
