import pathlib
import pygame
import queue as queue_lib
import random
import sys
import time

from models import Message
from utils import logger


class UltraManBeatMonsterGame:

    resource_dir = pathlib.Path(__file__).parent.parent.parent.joinpath('resources').resolve()

    def __init__(self, queue):
        # assert isinstance(queue, Queue)
        self.queue = queue

        self.window_size = 800, 600
        self.screen = pygame.display.set_mode(self.window_size)
        self.text = None

        self.image_hero_static = self._scale_image(self._load_image('game_outman_2.png'), (80, 120))
        self.image_hero_attack = self._scale_image(self._load_image('game_outman_3.png'), (80, 120))
        self.image_monster = self._scale_image(self._load_image('game_monster_2.png'), (80, 120))
        self.image_monster_part1 = self._scale_image(self._load_image('game_monster_2_1.png'), (80, 60))
        self.image_monster_part2 = self._scale_image(self._load_image('game_monster_2_0.png'), (80, 60))
        self.image_start_bg = self._load_image('game_outman_in.jpg')
        self.image_attack = self._scale_image(self._load_image('attack3.png', is_alpha=True), (680, 40))
        self.image_explode = self._scale_image(self._load_image('explode1.png', is_alpha=True), (180, 80))
        self.image_hand = None

        self.pos_start_bg = 60, 30
        self.pos_hero = 10, 240
        self.pos_monster = 660, 240
        self.pos_attack_from = (
            self.pos_hero[0] + self.image_hero_static.get_size()[0] / 3,
            self.pos_hero[1] + self.image_hero_static.get_size()[1] / 4
        )
        self.pos_attack_to = (
            self.pos_monster[0] + self.image_monster.get_size()[0] / 2,
            self.pos_monster[1] + self.image_monster.get_size()[1] / 2
        )

        self.pos_explode = (
            self.pos_monster[0] + self.image_monster.get_size()[0] / 2 - self.image_explode.get_size()[0] / 2,
            self.pos_monster[1] + self.image_monster.get_size()[1] / 2 - self.image_explode.get_size()[1] / 2
        )

        self.count_attack_to_destroy_monster = 800
        self.count_monster_number = 0
        self.count_score = 0

        self.ts_last_monster_generate = 0

    def _load_image(self, file_name, is_alpha=False):
        image_file = self.resource_dir.joinpath(file_name)
        assert image_file.exists()
        if is_alpha:
            return pygame.image.load(str(image_file.resolve())).convert_alpha()
        return pygame.image.load(str(image_file.resolve())).convert()

    @staticmethod
    def _scale_image(img, size=(100, 100)):
        return pygame.transform.scale(img, size)

    def random_generate_monster(self, ts):
        if self.count_monster_number > 0:
            return True
        if ts - self.ts_last_monster_generate > 3 and random.choice([True, False]):
            logger.critical('Generate a Monster!')
            self.ts_last_monster_generate = ts
            self.count_monster_number += 1
            return True
        return False

    def _run(self):
        pygame.init()
        self.text = pygame.font.SysFont('arial', 30)
        is_attacking = 0
        logger.critical('PyGame init success, starting...')
        start_ts = time.time()
        start_bg = True

        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            current_ts = time.time()
            if start_bg:
                if current_ts - start_ts <= 5:  # 开场背景展示一会儿
                    self.screen.blit(self.image_start_bg, self.pos_start_bg)
                    pygame.display.update()
                    continue
                else:
                    start_bg = False

            try:
                first_message = self.queue.get_nowait()
                assert isinstance(first_message, Message)
                if current_ts - first_message.timestamp >= 1:  # 延迟超过1s的就不要了
                    logger.warning('Got Delayed Message, Will Ignore!')
                    raise queue_lib.Empty
                if self.image_hand is None and first_message.mat_data is not None:
                    self.image_hand = pygame.surfarray.make_surface(first_message.mat_data)
            except queue_lib.Empty:
                first_message = None

            self.screen.fill(color=(0, 0, 0))
            score_text = self.text.render("Score: {}".format(self.count_score), False, (255, 0, 255))
            self.screen.blit(score_text, (350, 10))

            if not self.random_generate_monster(current_ts):
                is_attacking = 0
                self.screen.blit(self.image_hero_static, self.pos_hero)
                pygame.display.update()
                continue

            if is_attacking == 0 and first_message is not None and first_message.action == 'ATTACK':
                logger.critical(f'Got Attack Message: {first_message}')
                self.screen.blit(self.image_hero_attack, self.pos_hero)
                self.screen.blit(self.image_monster, self.pos_monster)
                self.screen.blit(self.image_attack, self.pos_attack_from)
                self.screen.blit(self.image_explode, self.pos_explode)
                # if self.image_hand is not None:
                #     self.screen.blit(self.image_hand, (350, 30))
                is_attacking += 1
            elif 0 < is_attacking <= self.count_attack_to_destroy_monster:

                # 最后4/5撕裂怪兽
                if is_attacking >= self.count_attack_to_destroy_monster * (2/3):
                    self.screen.blit(self.image_hero_attack, self.pos_hero)
                    # self.screen.blit(self.image_monster, self.pos_monster)
                    self.screen.blit(self.image_monster_part1, (self.pos_monster[0], self.pos_monster[1]-30))
                    self.screen.blit(self.image_monster_part2, (self.pos_monster[0], self.pos_monster[1]+60))
                    # self.screen.blit(self.image_attack, self.pos_attack_from)
                    self.screen.blit(self.image_explode, self.pos_explode)
                else:
                    self.screen.blit(self.image_hero_attack, self.pos_hero)
                    self.screen.blit(self.image_monster, self.pos_monster)
                    self.screen.blit(self.image_attack, self.pos_attack_from)
                    # self.screen.blit(self.image_explode, self.pos_explode)
                is_attacking += 1
                # if self.image_hand is not None:
                #     self.screen.blit(self.image_hand, (350, 30))
                if is_attacking >= self.count_attack_to_destroy_monster:
                    self.count_monster_number -= 1
                    self.count_score += 1
                    is_attacking = 0
                    self.image_hand = None
            else:
                is_attacking = 0
                self.screen.blit(self.image_hero_static, self.pos_hero)
                self.screen.blit(self.image_monster, self.pos_monster)

            pygame.display.update()
            if first_message is not None:
                logger.critical(f'Finish Draw {first_message}')

    def run(self):
        try:
            self._run()
        except Exception:
            logger.error('Failed to run, Error is:', exc_info=True)
            raise
