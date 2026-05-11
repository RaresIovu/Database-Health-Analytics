@echo off
echo Trimitem datele catre server...

curl -X POST http://127.0.0.1:5000/api/simulation/start ^
     -H "Content-Type: application/json" ^
     -d "{\"name\":\"Mouse\", \"price\":200}"

curl -X POST http://127.0.0.1:5000/api/simulation/stop ^
     -H "Content-Type: application/json" ^
     -d "{\"name\":\"Mouse\", \"price\":200}"

echo.
echo Operatiune finalizata.
pause