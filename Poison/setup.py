import subprocess
import sys

print("Installing requirements...")
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
except subprocess.CalledProcessError:
    print("❌ Failed to install requirements. Check your internet connection.")
    sys.exit(1)

print("Installing Playwright browsers...")
try:
    subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
except subprocess.CalledProcessError:
    print("❌ Failed to install Playwright browsers.")
    sys.exit(1)

print("\n✅ Setup complete! Run 'python main.py' to start.")

