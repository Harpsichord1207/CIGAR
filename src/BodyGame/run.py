import multiprocessing

from body_detect import BodyDetect
from game import UltraManBeatMonsterGame


def run_wrapper(clz, q):
    clz(q).run()


if __name__ == '__main__':
    message_queue = multiprocessing.Queue()

    multiprocessing.Process(target=run_wrapper, args=(BodyDetect, message_queue)).start()
    multiprocessing.Process(target=run_wrapper, args=(UltraManBeatMonsterGame, message_queue)).start()
