docker stop camera-01
docker rm camera-01
docker image rm camera-01:1.0
docker build -t camera-01:1.0 .
docker run --network=host --name camera-01 -d camera-01:1.0
