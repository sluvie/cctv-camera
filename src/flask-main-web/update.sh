docker stop camera-main-web
docker rm camera-main-web
docker image rm camera-main-web:1.0
docker build -t camera-main-web:1.0 .
docker run --network=host --name camera-main-web -d -p 9000:3001 camera-main-web:1.0
