import consul

session = consul.Consul()
session.kv.put("hz-nodes", "127.0.0.1:5701 127.0.0.1:5702 127.0.0.1:5703")
session.kv.put("log-map", "map")
session.kv.put("mes-queue", "queue")
