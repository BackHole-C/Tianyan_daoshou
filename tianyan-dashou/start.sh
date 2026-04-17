#!/bin/bash

# 启动Docker容器
echo "启动Docker容器..."
docker-compose up -d

echo "Docker容器启动完成！"
echo "前端访问地址: http://localhost"
echo "后端API地址: http://localhost/api"
echo "API文档地址: http://localhost/api/docs"