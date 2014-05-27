import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

setup(  name = "DragonSlayer",
        version = "0.0",
        description = "Blah",
        options = {"build_exe": build_exe_options},
        includefiles  = ["libV0_0", "drawings", "text", "re"],
        includes = ["re"], #use this to get rid of an unknown error
        executables = [Executable("dragonslayer.py", base=base)])
