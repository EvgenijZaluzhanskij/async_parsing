import random
import asyncio


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


async def launch_missile(delay, countdown):
    await asyncio.sleep(delay)

    for i in reversed(range(countdown)):
        print(f"{i + 1}...")
        await asyncio.sleep(1)
    print("Бесконечность не предел!")


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()

    tasks = [
        event_loop.create_task(launch_missile(d, c))
        for d, c in get_missiles()
    ]
    wait_tasks = asyncio.wait(tasks)

    event_loop.run_until_complete(wait_tasks)
    event_loop.close()
