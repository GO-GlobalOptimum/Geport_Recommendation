#!/bin/bash

docker build -t recsys:latest .
docker tag recsys taewan2002/recsys:latest
docker push taewan2002/recsys:latest