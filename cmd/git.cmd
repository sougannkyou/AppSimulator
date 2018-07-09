@ECHO OFF
echo now update source from git
cd %APPSIMULATOR_WORK_PATH%
git pull https://github.com/sougannkyou/AppSimulator.git
timeout 30
@ECHO ON