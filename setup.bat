@echo off
echo ============================================================
echo   Mafinho Explora - Setup do ambiente de desenvolvimento
echo ============================================================
echo.

REM 1. Verifica Python 3.11
python --version 2>nul | findstr "3.11" >nul
if errorlevel 1 (
    echo ERRO: Python 3.11 nao encontrado.
    echo Instale em: https://www.python.org/downloads/release/python-3119/
    pause
    exit /b 1
)
echo [1/4] Python 3.11 OK

REM 2. Cria o ambiente virtual
if not exist ".venv311" (
    echo [2/4] Criando ambiente virtual .venv311...
    python -m venv .venv311
) else (
    echo [2/4] .venv311 ja existe, pulando criacao
)

REM 3. Instala TTS com contorno do bug setuptools (necessario apenas uma vez)
echo [3/4] Instalando TTS ^(pode demorar ~30 min na primeira vez^)...
.venv311\Scripts\python.exe install_tts.py
if errorlevel 1 (
    echo ERRO na instalacao do TTS. Veja mensagens acima.
    pause
    exit /b 1
)

REM 4. Instala demais dependencias
echo [4/4] Instalando demais dependencias...
.venv311\Scripts\pip.exe install -r requirements.txt

echo.
echo ============================================================
echo   Ambiente pronto!
echo   Proximo passo: copie seu arquivo .env para esta pasta
echo   Conteudo necessario:
echo     GEMINI_API_KEY=sua_chave_aqui
echo     HF_TOKEN=seu_token_aqui
echo ============================================================
pause
