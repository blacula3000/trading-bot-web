#!/bin/bash
git pull
docker build -t trading-bot-web .
docker stop $(docker ps -q --filter ancestor=trading-bot-web) || true
docker run -d -p 80:5000 trading-bot-web
