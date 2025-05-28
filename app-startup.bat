@echo off
setlocal

where python >nul 2>&1
if errorlevel 1 (
    echo Python nie jest zainstalowany lub nie jest w PATH.
    pause
    exit /b 1
)

python -m venv .venv

call .venv\Scripts\activate


if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo Brak pliku requirements.txt
    pause
    exit /b 1
)

flask --app app run --debug


pause

deactivate

endlocal

pause

