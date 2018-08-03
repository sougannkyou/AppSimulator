cd %APPSIMULATOR_WORK_PATH%
TIMEOUT 60
START "WebServer" cmd\WebStart.cmd
TIMEOUT 10
START "Multi Nox Monitor" python Controller\NoxMonitor.py
