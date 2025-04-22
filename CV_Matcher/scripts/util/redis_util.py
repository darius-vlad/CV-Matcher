from time import sleep

import redis

HOST = 'localhost'
PORT = 6379

redis_client = redis.StrictRedis(host=HOST, port=PORT, db=0)
deque_key = "queue"

def dequeue_id():
    return redis_client.lpop(deque_key)

if __name__ == '__main__':
    while True:
        id = dequeue_id()
        print(id)
        sleep(10)

    # open redis-cli
    # LPUSH queue 123
    # LPUSH queue 456
    # LPUSH queue 789
    # and the program should retrieve the ids one by one