docker stop camera-02
docker rm camera-02
docker image rm camera-02:1.0
docker build -t camera-02:1.0 .
docker run --network=host --name camera-02 -d camera-02:1.0
#docker run --name camera-02 -d -p 3003:3001 camera-02:1.0
