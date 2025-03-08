import subprocess

with open('requirements.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):  # Skip empty lines and comments
            print(f"Attempting to install: {line}")
            try:
                subprocess.check_call(['pip', 'install', line])
            except subprocess.CalledProcessError as e:
                print(f"  Failed to install: {line} (ignoring error and continuing)")
                print(f"  Error details: {e}")