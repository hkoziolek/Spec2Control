@echo off
REM Spec2Control CLI Wrapper Script
REM Runs the CLI tool from the root directory with argument passthrough

cd /d "%~dp0src"
python spec2control_cli.py %*
