@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x64
if errorlevel 1 (
    echo VCVARSALL FAILED
    exit /b 1
)
REM Add Windows SDK bin to PATH for rc.exe
set "PATH=C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64;%PATH%"
echo VCVARSALL OK
echo Installing TTS...
"%~dp0.venv311\Scripts\pip.exe" install "TTS==0.22.0" --no-build-isolation
