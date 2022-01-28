import pathlib
import pygame
import queue as queue_lib
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

        self.image_hero = self._scale_image(self._load_image('game_outman.png'), (80, 120))
        self.image_monster = self._scale_image(self._load_image('game_monster.jpg'), (80, 120))
        self.image_start_bg = self._load_image('game_outman_in.jpg')

        self.image_attack = self._scale_image(self._load_image('attack2.png', is_alpha=True), (680, 40))
        self.image_explode = self._scale_image(self._load_image('explode1.png', is_alpha=True), (180, 80))

        self.pos_start_bg = 60, 30
        self.pos_hero = 10, 240
        self.pos_monster = 660, 240
        self.pos_attack_from = (
            self.pos_hero[0] + self.image_hero.get_size()[0] / 3,
            self.pos_hero[1] + self.image_hero.get_size()[1] / 4
        )
        self.pos_attack_to = (
            self.pos_monster[0] + self.image_monster.get_size()[0] / 2,
            self.pos_monster[1] + self.image_monster.get_size()[1] / 2
        )

        self.pos_explode = (
            self.pos_monster[0] + self.image_monster.get_size()[0] / 2 - self.image_explode.get_size()[0] / 2,
            self.pos_monster[1] + self.image_monster.get_size()[1] / 2 - self.image_explode.get_size()[1] / 2
        )

    def _load_image(self, file_name, is_alpha=False):
        image_file = self.resource_dir.joinpath(file_name)
        assert image_file.exists()
        if is_alpha:
            return pygame.image.load(str(image_file.resolve())).convert_alpha()
        return pygame.image.load(str(image_file.resolve())).convert()

    @staticmethod
    def _scale_image(img, size=(100, 100)):
        return pygame.transform.scale(img, size)

    def _run(self):
        pygame.init()
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
            except queue_lib.Empty:
                first_message = None

            if is_attacking == 0 and first_message is not None and first_message.action == 'ATTACK':
                logger.critical(f'Got Attack Message: {first_message}')
                self.screen.blit(self.image_hero, self.pos_hero)
                self.screen.blit(self.image_monster, self.pos_monster)
                self.screen.blit(self.image_attack, self.pos_attack_from)
                self.screen.blit(self.image_explode, self.pos_explode)
                is_attacking += 1
            elif 0 < is_attacking <= 100:
                self.screen.blit(self.image_hero, self.pos_hero)
                self.screen.blit(self.image_monster, self.pos_monster)
                self.screen.blit(self.image_attack, self.pos_attack_from)
                self.screen.blit(self.image_explode, self.pos_explode)
                is_attacking += 1
            else:
                self.screen.fill(color=(0, 0, 0))
                is_attacking = 0
                self.screen.blit(self.image_hero, self.pos_hero)
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
