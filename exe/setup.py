from cx_Freeze import setup, Executable  
import sys
import os

build_exe_options = {"excludes": ["tkinter"],
                     "packages": ["idna"],
                     "include_files": ["logo.png"],
                     "optimize": 2}  

base = None  
if sys.platform == "win32":  
    base = "Win32GUI"  

os.chdir("..")

setup(
    name="AoD",  
    version="1.0",  
    description="Description",  
    options={"build_exe": build_exe_options},  
    executables=[Executable("AoD.py", base=base, icon="exe/icon.ico")]
    )  

