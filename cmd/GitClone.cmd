@ECHO OFF
echo now clone projext from git
cd %APPSIMULATOR_WORK_PATH%\..
RMDIR /Q /S AppSimulator
REM C:\Git\bin\git pull https://github.com/sougannkyou/AppSimulator.git
C:\Git\bin\git clone https://github.com/sougannkyou/AppSimulator.git
timeout 30
@ECHO ON