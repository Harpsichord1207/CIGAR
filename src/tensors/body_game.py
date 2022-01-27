import cv2
import mediapipe as mp
import sys
import threading
import time
import pygame


class Message:

    def __init__(self, action, timestamp=None):
        self.timestamp = timestamp or time.time()
        self.action = action

    def __str__(self):
        return f'Message[{self.action}/{self.timestamp}]'


class MessageQueue:

    # TODO: 使用真正的休息队列
    def __init__(self):
        self.data = []

    def first(self):
        data = []
        m = None
        for message in self.data:
            assert isinstance(message, Message)
            if time.time() - message.timestamp > 2:  # 消息延迟超过2秒
                continue
            if m is None:
                m = message
            else:
                data.append(message)
        self.data = data
        return m

    def put(self, message):
        if not self.data:
            self.__put(message)
            return
        prev_message = self.data[-1]
        if message.action == prev_message.action and message.timestamp - prev_message.timestamp <= 1:
            # 1秒内相同的指令不处理
            return
        self.__put(message)

    def __put(self, message):
        self.data.append(message)
        print(f'{time.time()}: 收到指令: {message}, 当前Queue大小: {len(self.data)}')


def run_game(message_queue):

    assert isinstance(message_queue, MessageQueue)
    pygame.init()
    size = width, height = 800, 600

    screen = pygame.display.set_mode(size)
    hero_img = pygame.image.load(r'D:\Projects\Py\CIGAR\resources\game_outman.png').convert()
    hero_img = pygame.transform.scale(hero_img, (80, 120))

    monster_img = pygame.image.load(r'D:\Projects\Py\CIGAR\resources\game_monster.jpg').convert()
    monster_img = pygame.transform.scale(monster_img, (80, 120))

    is_attacking = 0

    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        first_message = message_queue.first()
        if is_attacking == 0 and first_message is not None and first_message.action == 'ATTACK':
            print(f'{time.time()}: 收到攻击指令->{first_message}！')
            screen.blit(hero_img, (10, 240))
            screen.blit(monster_img, (660, 240))
            pygame.draw.rect(screen, (17, 238, 238), (36, 270, 700, 20), 10)
            is_attacking += 1
        elif 0 < is_attacking <= 100:
            # print('持续攻击中！')
            screen.blit(hero_img, (10, 240))
            screen.blit(monster_img, (660, 240))
            pygame.draw.rect(screen, (17, 238, 238), (36, 270, 700, 20), 10)
            is_attacking += 1
        else:
            # print('停止攻击！')
            screen.fill(color=(0, 0, 0))
            screen.blit(hero_img, (10, 240))
            screen.blit(monster_img, (660, 240))
            is_attacking = 0

        pygame.display.update()
        pygame.display.flip()


def run_detect(message_queue):
    assert isinstance(message_queue, MessageQueue)
    pose = mp.solutions.pose.Pose()
    mp_drawer = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    ts = 0

    right_hand_points = {16, 18, 20, 22}
    left_hand_points = {15, 17, 19, 21}
    while True:
        success, img = cap.read()
        if not success:
            continue
        pose_results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not pose_results:
            # TODO: 这种情况画面也不动了
            continue

        h, w, c = img.shape
        mp_drawer.draw_landmarks(img, pose_results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        current_points = set()
        for _id, lm in enumerate(pose_results.pose_landmarks.landmark):
            if _id not in (right_hand_points | left_hand_points):
                continue
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
            cv2.putText(img, str(_id), (cx+5, cy+5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            if lm.visibility >= 0.65 and (_id in right_hand_points or _id in left_hand_points):
                current_points.add(_id)

        if current_points & right_hand_points == right_hand_points:
            attack_message = Message(action='ATTACK')
            message_queue.put(attack_message)
            print(f'I am here {time.time()}')
        if current_points & left_hand_points == left_hand_points:
            defend_message = Message(action='DEFEND')
            message_queue.put(defend_message)

        c_ts = time.time()
        fps = 1 / (c_ts - ts)
        ts = c_ts
        cv2.putText(img, str(round(fps, 2)), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("ActionCamera", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    # TODO: 使用进程：https://www.cnblogs.com/guguobao/p/9398653.html
    global_message_queue = MessageQueue()
    threads = [
        threading.Thread(target=run_game, args=(global_message_queue,)),
        threading.Thread(target=run_detect, args=(global_message_queue,))
    ]
    for t in threads:
        # 启动线程
        t.start()
