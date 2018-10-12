@ECHO OFF
echo now pull source from git
cd %APPSIMULATOR_WORK_PATH%
C:\Git\bin\git pull
timeout 30
@ECHO ON