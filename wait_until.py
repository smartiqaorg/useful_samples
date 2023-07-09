import time


def wait_until(condition, description, timeout=300, period=0.25, *args, **kwargs):
    final_time = time.time() + timeout
    while time.time() < final_time:
        if condition(*args, **kwargs):
            return True
        time.sleep(period)
    raise TimeoutError(f'Timed out waiting for condition: [{description}]')


def closure(n):

    def sleep_several_seconds():
        nonlocal n
        time.sleep(1)
        n = n - 1
        print(f"{n} seconds left")
        return n

    return sleep_several_seconds


def five_seconds_passed():
    return sleep_five_seconds() == 0


sleep_five_seconds = closure(5)

wait_until(condition=five_seconds_passed, description='Five seconds are over', timeout=3)
