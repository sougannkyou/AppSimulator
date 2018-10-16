cd %APPSIMULATOR_WORK_PATH%
TASKKILL /F /T /FI "WINDOWTITLE eq WebServer - cmd\WebStart.cmd"
TASKKILL /F /T /FI "WINDOWTITLE eq Multi Nox Monitor"
TIMEOUT 60
START "WebServer" cmd\WebStart.cmd
TIMEOUT 10
START "Multi Nox Monitor" python Controller\NoxMonitor.py
