docker run \
    -d \
    --net=host \
    -p 8500:8500 \
    -p 8600:8600/udp \
    --name=micro_consul \
    consul agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0

sleep 5

python3 consul_conf.py