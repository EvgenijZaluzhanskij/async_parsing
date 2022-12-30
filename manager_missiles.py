import time
import heapq
import random
from enum import Enum, auto


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


class Operation(Enum):
    WAIT = auto()
    STOP = auto()


class State(Enum):
    WAITING = auto()
    WORKING = auto()
    LAUNCHING = auto()


class Launch:
    def __init__(self, delay, countdown):
        self._delay = delay
        self._countdown = countdown
        self._state = State.WAITING

    def step(self):
        if self._state is State.WAITING:
            self._state = State.WORKING
            return Operation.WAIT, self._delay

        if self._state is State.WORKING:
            if self._countdown == 0:
                self._state = State.LAUNCHING
            else:
                print(f"""{self._countdown}...""")
                self._countdown -= 1
                return Operation.WAIT, 1

        if self._state is State.LAUNCHING:
            print("Бесконечность не предел!")
            return Operation.STOP, None


def now():
    return time.time()


def armageddon(missiles):
    start = now()

    jobs = [
        (start, i, Launch(d, c)) for i, (d, c) in enumerate(missiles)
    ]

    while jobs:
        step_at, missile_id, job = heapq.heappop(jobs)
        wait = step_at - now()
        if wait > 0:
            time.sleep(wait)

        op, wait_delta = job.step()
        if op is Operation.WAIT:
            step_at = now() + wait_delta
            heapq.heappush(jobs, (step_at, missile_id, job))


if __name__ == "__main__":
    armageddon(get_missiles())
