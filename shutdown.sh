#!/bin/bash

# 查找监听8481端口的进程PID
pid=$(lsof -i :8481 | awk 'NR>1 {print $2}')

# 如果找到了PID，则尝试杀死进程
if [ -n "$pid" ]; then
    echo "Stopping application of 8481 port with PID $pid..."
    kill $pid
    echo "Application stopped."
else
    echo "No process found listening on port 8481."
fi