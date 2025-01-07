from cx_Freeze import setup, Executable

setup(name="PNG to OBJ", executables=[Executable("PNG to OBJ.py")], options={"build_exe": {"excludes": ["tkinter"]}})