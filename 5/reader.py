import hazelcast
from time import sleep

if __name__ == "__main__":
    client = hazelcast.HazelcastClient()
    bound_queue = client.get_queue("bounded-queue").blocking()

    for i in range(1000):
        value = bound_queue.take()

        print("Reading:", value)
        sleep(0.01)

        if value == -1:
            bound_queue.put(value)
            break

    print("Reader finished!")

    client.shutdown()
