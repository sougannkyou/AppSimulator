TIMEOUT 60
cd %APPSIMULATOR_WORK_PATH%\cmd
VMClone.cmd
TIMEOUT 60
START "WebServer" WebStart.cmd
START "VMware Screen Capture" VMScreenCapture.cmd