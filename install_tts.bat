@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x64 >nul 2>&1
"C:\Users\paulo\OneDrive\td junto outlook hotmail\Mafinho\app_marcelo\.venv311\Scripts\pip.exe" install "TTS==0.22.0" pydub
