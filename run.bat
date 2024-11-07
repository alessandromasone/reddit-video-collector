py main.py

@echo off
rem Questo script rimuove tutte le cartelle __pycache__ ricorsivamente

for /r %%i in (__pycache__) do (
    if exist "%%i" rd /s /q "%%i"
)

