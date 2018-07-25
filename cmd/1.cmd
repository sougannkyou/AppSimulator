
FOR %%i in (1,2,3,4,5) DO CALL :LOOP_VM
GOTO :EOF

:LOOP_VM
FOR %%vm in (vm1,vm2,vm5) (
   echo %vm%
)
GOTO :EOF
::--------------------------------------------------
:END
ECHO ON