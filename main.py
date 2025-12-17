
import subprocess
import sys
import os

def main():
    """
    Runs the Streamlit application.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Construct the absolute path to the Streamlit app
    app_path = os.path.join(script_dir, "src", "ui", "streamlit", "app.py")
    
    # Command to run the streamlit app
    command = [sys.executable, "-m", "streamlit", "run", app_path]
    
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command)

if __name__ == "__main__":
    main()
