#!/bin/bash

# AI_main.py와 Middleware_main.py를 백그라운드에서 실행
python vital_server.py &
python user_server.py &

# 모든 백그라운드 프로세스가 완료될 때까지 기다립니다.
wait