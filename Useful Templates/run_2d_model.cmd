@echo off
REM Usage: win_scr.cmd <full path to dir with fields> <relative path to js file>
for /f "tokens=2 delims=:." %%x in ('chcp') do set cp=%%x
chcp 1251>nul
SET TRIK_DIR=%~dp0
SET FIELDS_PATH=%1
echo %FIELDS_PATH%
SET DEFAULT_PROJECT=%FIELDS_PATH%\default.qrs
IF EXIST %DEFAULT_PROJECT% (
	SET PROJECT_TYPE=xml
) ELSE (
	SET PROJECT_TYPE=qrs
)
SET mydir=%cd%
pushd "%FIELDS_PATH%"
echo %mydir%\%2
for %%f in (*.%PROJECT_TYPE%) do (
	IF "%PROJECT_TYPE%"=="xml" (
		echo "%%f"
		"%TRIK_DIR%patcher.exe" -f %%f "%DEFAULT_PROJECT%"
		"%TRIK_DIR%patcher.exe" -s "%mydir%\%2" "%DEFAULT_PROJECT%"
		"%TRIK_DIR%2D-model.exe" --mode script -c "%DEFAULT_PROJECT%"
	)
	IF "%PROJECT_TYPE%"=="qrs" (
		echo "%%f"
		"%TRIK_DIR%patcher.exe" -s "%mydir%\%2" %%f 
		"%TRIK_DIR%2D-model.exe" --mode script -c %%f
	)
)
chcp %cp%>nul
popd