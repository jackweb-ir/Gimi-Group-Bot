import subprocess
import sys

def install(libraries):
    for library in libraries:
        try:
            
            __import__(library)
            print(f">>>> library : {library} Already installed.")
            
        except ImportError:
            
            print(f">>>> library : {library} Not installed. Installing...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])


