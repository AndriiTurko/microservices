import hazelcast
from time import sleep

if __name__ == "__main__":
    client = hazelcast.HazelcastClient()
    bound_queue = client.get_queue("bounded-queue").blocking()

    for i in range(1000):
        bound_queue.put(i)

        print("Writing:", i)
        sleep(0.01)

    bound_queue.put(-1)
    print("Writer finished!")

    client.shutdown()
