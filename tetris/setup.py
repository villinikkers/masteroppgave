
from cx_Freeze import setup, Executable
import os.path
import sys


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
files = ["highscorebeaten.wav", "gameover.wav", "levelup.wav", "linecleared.wav"]
# Dependencies are aytomatically detected, but it might need fine tuning.
build_exe_options = {
                    "packages": ["os", "pygame"],
                    "include_files": files,
                    "excludes": ["tkinter", "scipy"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    name="Tetris",
    description = "Tetris multiple modes.",
    version="0.1",
    options={'build_exe': build_exe_options},
    executables = [Executable('guiTest.py', icon = 'brain-tetris.ico')]
)
