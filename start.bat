@echo off

echo 🚀 Starting E-commerce Microservices...
docker-compose up -d --build

echo.
echo ================================
echo ✅ RUNNING CONTAINERS:
echo ================================

docker ps --format "table {{.Names}}\t{{.Ports}}"

echo ================================
echo 🌐 Access URLs:
echo ================================
echo Frontend: http://localhost:3000
echo Swagger:  http://localhost:8000/docs
echo ================================

pause