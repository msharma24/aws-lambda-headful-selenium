#!/bin/bash
 echo "[INFO] using AWS Region us-west-2"
 echo "[INFO] Change this script for your env"

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 686401449244.dkr.ecr.us-west-2.amazonaws.com
docker build -t dev-selenium-ecr .
docker tag dev-selenium-ecr:latest 686401449244.dkr.ecr.us-west-2.amazonaws.com/dev-selenium-ecr:latest
docker push 686401449244.dkr.ecr.us-west-2.amazonaws.com/dev-selenium-ecr:latest
