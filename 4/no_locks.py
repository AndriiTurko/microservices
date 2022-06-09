import hazelcast
import time

if __name__ == "__main__":
    client = hazelcast.HazelcastClient()
    dist_map = client.get_map("my-distributed-map").blocking()

    key = "1"
    value = 0
    dist_map.put_if_absent(key, value)

    start = time.time()

    for i in range(1000):
        value = dist_map.get(key)
        time.sleep(0.01)
        value += 1
        dist_map.put(key, value)

    print("Result:", dist_map.get(key), "time:", time.time() - start)

    client.shutdown()
