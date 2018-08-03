cd %APPSIMULATOR_WORK_PATH%
TIMEOUT 60
START "Revert All VMware" cmd\VMClone.cmd
TIMEOUT 1200
START "VMware Screen Capture" cmd\VMScreenCapture.cmd
TIMEOUT 10
START "WebServer" cmd\WebStart.cmd
TIMEOUT 10
START "VMware Monitor" python Controller\VMMonitor.py