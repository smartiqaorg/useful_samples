import time

RETRIES = 3
TIMEOUT = 60
PERIOD = 5


def retry(max_retries, timeout, period):
    def outer(func):
        def inner(*args, **kwargs):
            end_time = time.time() + timeout
            retries = max_retries
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f'{e}')
                    if time.time() > end_time:
                        raise 'Timeout has expired!'
                    if retries == 1:
                        raise e
                    else:
                        retries -= 1
                        print(f"Attempts left: {retries}")
                        print(f"Sleeping {period} seconds ...")
                        time.sleep(period)
        return inner
    return outer


@retry(RETRIES, TIMEOUT, PERIOD)
def send_request():
    raise Exception('Code block has failed. This is expected.')


# Tests
send_request()
