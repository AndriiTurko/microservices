import hazelcast

if __name__ == "__main__":
    hz = hazelcast.HazelcastClient()

    hz_map = hz.get_map("my-distributed-map").blocking()

    for i in range(1000):
        hz_map.put(i, "value")

    hz.shutdown()
