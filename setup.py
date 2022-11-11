from cx_Freeze import setup, Executable

setup(name="Object Detection Solution",version="1.0",
description="This software detects objects in realtime",
executables=[Executable("D:\Python Practice\Image processing\object detection\main.py")])