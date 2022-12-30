import time
import heapq
import random


def now():
    return time.time()


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


def sleep(delay):
    return delay


def launch_missile(delay, countdown):
    yield sleep(delay)

    for i in reversed(range(countdown)):
        print(f"{i + 1}...")
        yield sleep(1)
    print("Бесконечность не предел!")


def armageddon(missiles):
    start = now()

    jobs = [
        (start, i, launch_missile(d, c)) for i, (d, c) in enumerate(missiles)
    ]

    while jobs:
        step_at, missile_id, job = heapq.heappop(jobs)
        wait = step_at - now()
        if wait > 0:
            time.sleep(wait)

        try:
            wait_delta = job.send(None)
        except StopIteration:
            continue

        step_at = now() + wait_delta
        heapq.heappush(jobs, (step_at, missile_id, job))


if __name__ == "__main__":
    armageddon(get_missiles())
