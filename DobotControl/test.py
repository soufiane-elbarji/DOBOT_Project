import subprocess

# Full path to Python 3.5.0 interpreter
python35_path = "C:\\Users\\pc\\AppData\\Local\\Programs\\Python\\Python35\\python.exe"  # Adjust this to your actual path
script_to_run = "DobotControl\\DobotDrawer.py" # Your Python 3.5 script

# Run the script with Python 3.5
subprocess.run([python35_path, script_to_run])
