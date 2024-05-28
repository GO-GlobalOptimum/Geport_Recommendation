#!/bin/bash

docker build -t recsys:latest .
docker tag recsys:latest
docker push recsys:latest