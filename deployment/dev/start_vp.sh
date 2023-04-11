#! /usr/bin/bash
docker-compose -f ~/DevMentoring/vpscrap/deployment/dev/docker-compose.yml up --build -d
docker-compose -f ~/DevMentoring/vpcore/deployment/dev/docker-compose.yml up --build -d
