"""
install_tts.py — Instala Coqui TTS 0.22.0 no Windows contornando bug do setuptools.

Causa raiz: setuptools 82.x usa `cmd /u` (UTF-16LE) para detectar MSVC,
o que corrompe a saída do vcvarsall.bat → PATH vazio → rc.exe não encontrado.

Solução: capturamos o env do vcvarsall.bat nós mesmos (via `cmd /c`, encoding
correto) e setamos DISTUTILS_USE_SDK=1, que faz o setuptools pular toda a
detecção automática e usar as variáveis de ambiente que já fornecemos.
Ref: setuptools/msvc.py linhas 150-151
"""
import os
import subprocess
import sys


def get_vcvarsall_env():
    """Executa vcvarsall.bat e captura todas as variáveis de ambiente resultantes."""
    vcvarsall = r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat"
    if not os.path.exists(vcvarsall):
        print(f"ERRO: vcvarsall.bat nao encontrado em:\n  {vcvarsall}")
        print("Instale Visual Studio Build Tools 2022 com C++ workload.")
        sys.exit(1)

    # Usa cmd /c (NÃO /u) para evitar o bug de encoding UTF-16LE
    cmd = f'cmd.exe /c "call "{vcvarsall}" x64 >nul 2>&1 && set"'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print("ERRO: vcvarsall.bat falhou")
        print(result.stderr)
        sys.exit(1)

    env = {}
    for line in result.stdout.splitlines():
        if "=" in line:
            key, _, value = line.partition("=")
            env[key] = value
    return env


def check_tools(env):
    """Verifica se cl.exe, link.exe e rc.exe estão no PATH."""
    path_dirs = env.get("PATH", "").split(";")
    tools = {}
    for tool in ["cl.exe", "link.exe", "rc.exe"]:
        tools[tool] = any(
            os.path.exists(os.path.join(d, tool))
            for d in path_dirs if d.strip()
        )
        status = "OK" if tools[tool] else "NAO ENCONTRADO"
        print(f"  {tool}: {status}")

    # Adiciona SDK bin se rc.exe não está no PATH
    if not tools["rc.exe"]:
        sdk_bin = r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64"
        if os.path.exists(os.path.join(sdk_bin, "rc.exe")):
            env["PATH"] = sdk_bin + ";" + env.get("PATH", "")
            print(f"  rc.exe: adicionado {sdk_bin} ao PATH")
            tools["rc.exe"] = True

    return all(tools.values())


def check_ffmpeg(env):
    """Verifica se ffmpeg esta disponivel, incluindo locais do winget."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, env=env)
        print("  ffmpeg: OK")
        return True
    except FileNotFoundError:
        pass

    # Procura no diretorio do winget
    import glob
    winget_pattern = os.path.expanduser(
        "~/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg*/*/bin"
    )
    matches = glob.glob(winget_pattern)
    if matches:
        ffmpeg_bin = matches[0]
        if os.path.exists(os.path.join(ffmpeg_bin, "ffmpeg.exe")):
            env["PATH"] = ffmpeg_bin + ";" + env.get("PATH", "")
            print(f"  ffmpeg: OK (adicionado {ffmpeg_bin} ao PATH)")
            return True

    print("  ffmpeg: NAO ENCONTRADO")
    print("  Instale com: winget install Gyan.FFmpeg")
    return False


def main():
    print("=" * 60)
    print("  Mafinho Explora — Instalador TTS (XTTS-v2)")
    print("=" * 60)

    # 1. Captura ambiente MSVC
    print("\n[1/4] Configurando ambiente MSVC via vcvarsall.bat...")
    env = get_vcvarsall_env()

    # 2. Verifica ferramentas
    print("\n[2/4] Verificando ferramentas de build...")
    if not check_tools(env):
        print("\nERRO: Ferramentas MSVC incompletas. Instale Build Tools 2022.")
        sys.exit(1)

    # DISTUTILS_USE_SDK=1 faz setuptools pular detecção MSVC (contorna bug)
    env["DISTUTILS_USE_SDK"] = "1"
    print("  DISTUTILS_USE_SDK=1 (contorna bug setuptools encoding)")

    # 3. Verifica ffmpeg
    print("\n[3/4] Verificando ffmpeg...")
    if not check_ffmpeg(env):
        print("\nAVISO: ffmpeg necessario para converter amostras MP4 para WAV.")
        print("Continuando instalacao do TTS, mas gerar vozes vai falhar sem ffmpeg.\n")

    # 4. Instala TTS
    print("\n[4/4] Instalando TTS==0.22.0...")
    pip = os.path.join(os.path.dirname(sys.executable), "pip.exe")
    if not os.path.exists(pip):
        pip = os.path.join(os.path.dirname(sys.executable), "Scripts", "pip.exe")
    cmd = [pip, "install", "TTS==0.22.0", "--no-build-isolation"]

    print(f"  Comando: {' '.join(cmd)}")
    print("=" * 60)

    result = subprocess.run(cmd, env=env)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("  TTS instalado com sucesso!")
        print("  Proximo passo: python generate_voices.py --test")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("  ERRO na instalacao do TTS.")
        print("  Verifique os logs acima para detalhes.")
        print("=" * 60)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
