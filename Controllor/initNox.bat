cd "c:\\Nox\\bin"
NoxConsole quitall
NoxConsole list
FOR %%i IN (1,2,3,4,5,6,7,8,9,10) do NoxConsole remove -name:nox-%%i && timeout 5
FOR %%i IN (1,2,3,4,5,6,7,8,9,10) do NoxConsole copy -name:nox-%%i -from:org && timeout 20
FOR %%i IN (1,2,3,4,5,6,7,8,9,10) do NoxConsole restore -name:nox-%%i -file:"C:\Nox\backup\nox-dianping.npbk" && timeout 20

pause

