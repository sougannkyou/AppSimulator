TIMEOUT 60
cd %APPSIMULATOR_WORK_PATH%\cmd
START "Revert All VMware" VMClone.cmd
TIMEOUT 1200
START "VMware Screen Capture" VMScreenCapture.cmd
TIMEOUT 10
START "WebServer" WebStart.cmd
