docker build -t needle-fe:latest .
docker tag needle-fe:latest **.**.cn/ai/needle-fe:latest
docker login -u ai -p your_pwd **.**.cn
docker push **.**.cn/ai/needle-fe:latest
