from sys import argv

files = argv[1:]

exeString = [f"Executable('{file}', icon = 'brain-tetris.ico')" for file in files]
exeString2 = "["

for item in exeString:
  exeString2 += item + ","

exeString2 = exeString2[:-1]
exeString2 += ']'

print(exeString2)
setup_script=f"""
from cx_Freeze import setup, Executable
import os.path
import sys


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
files = ["highscorebeaten.wav", "gameover.wav", "levelup.wav", "linecleared.wav"]
# Dependencies are aytomatically detected, but it might need fine tuning.
build_exe_options = {{
                    "packages": ["os", "pygame"],
                    "include_files": files,
                    "excludes": ["tkinter", "scipy"]}}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    name="Tetris",
    description = "Tetris multiple modes.",
    version="0.1",
    options={{'build_exe': build_exe_options}},
    executables = {exeString2}
)
"""

with open('setup.py', 'w') as f:
  f.write(setup_script)
