@ECHO OFF
echo now update source from git
cd %APPSIMULATOR_WORK_PATH%\..
DEL /F /Q /S AppSimulator
REM C:\Git\bin\git pull https://github.com/sougannkyou/AppSimulator.git
C:\Git\bin\git clone https://github.com/sougannkyou/AppSimulator.git
timeout 30
@ECHO ON