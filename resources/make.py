from sys import argv
from sys import path as spath

spath.append("resources/circuitmpy")
from circuitmpy import compile_mpy

try:
    compile_mpy("src/ramdisk.py", "ramdisk.mpy", optim=3)
except OSError:
    print("Compilation error, exiting")
    exit(1)
