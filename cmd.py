import subprocess
import os
from setup import compile

path = os.getcwd()
get_files = os.listdir(path)
print get_files
files_list = []


class compiled():
    def __init__(self):
        self.cmd()

    def cmd(self):
        try:
            subprocess.call(["python", "setup.py", "build_ext", "-b", "compiled_pyd_files"])
        except:
            pass


if __name__ == "__main__":
    compiled()
