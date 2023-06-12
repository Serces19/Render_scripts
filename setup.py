import sys
import os
from cx_Freeze import setup, Executable

files = ['recursos', 'controladores', 'ui']

exe = Executable(script="app_dev.py", base="Win32GUI", icon="E:/Code/Render/recursos/logo_s.ico")

setup(
    name = "Render_all!",
    version = "1.0",
    description = "App for render multiple nuke files in one",
    author = "Sergio Cespedes",
    options = {'build_exe': {'include_files': files}},
    executables = [exe]
)
