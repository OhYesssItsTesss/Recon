import os
import subprocess
import sys
import shutil

def check_pyinstaller():
    try:
        import PyInstaller
        print("[+] PyInstaller is installed.")
    except ImportError:
        print("[!] PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build():
    print("--- Building Recon Executable ---")
    
    # Clean previous builds
    if os.path.exists("dist"): shutil.rmtree("dist")
    if os.path.exists("build"): shutil.rmtree("build")

    # Command explanation:
    # --onefile: Bundle everything into one .exe
    # --name: Output name
    # --add-data: We might need to add templates or config files if we had them
    # --hidden-import: Explicitly import hidden dependencies like rich or google-genai submodules
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=Recon",
        "--clean",
        "--hidden-import=rich",
        "--hidden-import=keyring.backends.Windows",
        "src/cli.py"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    
    print("\n[✔] Build Complete!")
    print(f"Executable is located at: {os.path.abspath('dist/Recon.exe')}")

if __name__ == "__main__":
    check_pyinstaller()
    build()
