@echo off
:loop
REM Intervalo aleatorio entre 3 y 4 horas (10800 a 14400 segundos)
set /a delay=%random% %% 36 + 36

REM Muestra cuánto tiempo esperará antes de ejecutar el próximo comando
echo Esperando %delay% segundos antes de ejecutar el comando...

REM Espera el intervalo aleatorio
timeout /t %delay% /nobreak

REM Ejecuta el script principal
call "E:\TEST TIME\docker_runner.bat"

REM Vuelve al inicio del bucle
goto loop
