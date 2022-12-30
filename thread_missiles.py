import time
import random

from threading import Thread


def random_delay():
    return random.random() * 5


def random_countdown():
    return random.randrange(5)


def get_missiles():
    missiles_count = 10_000

    return [
        (random_delay(), random_countdown())
        for _ in range(missiles_count)
    ]


def launch_missile(delay, countdown):
    time.sleep(delay)

    for i in reversed(range(countdown)):
        print(f"{i + 1}...")
        time.sleep(1)
    print("Бесконечность не предел!")


def run_threads():
    threads = [
        Thread(target=launch_missile, args=(d, c))
        for d, c in get_missiles()
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    run_threads()
