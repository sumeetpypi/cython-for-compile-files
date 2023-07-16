from setuptools import setup
from setuptools.extension import Extension
# from compilied_projects_main import compliled_project
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import glob
import os
import fnmatch
import distutils.dir_util
import shutil

files_list = []
get_files = dict()
folder = []


class compile():
    def __init__(self):
        self.compilation()

    def get_current_dir(self):
        current_dir = os.getcwd()
        return current_dir

    def compilation(self):
        current_dir = self.get_current_dir()
        #get_path = compliled_project.current_dir_path()

        get = os.listdir(self.get_current_dir())

        if ".git" in get:
            get.remove('.git')

        if ".idea" in get:
            get.remove('.idea')

        for x in glob.glob('**/__init__.py'):
            os.remove(x)

        for y in glob.glob('**/.git'):
            os.remove(y)

        for root, dirs, files in os.walk(self.get_current_dir()):
            for file in files:
                print ">>>>>>>> check file",file
                if file.endswith(".py"):
                    files_list.append(os.path.join(root, file))
                    get_files[dir] = file

        for paths in files_list:
            if not paths.endswith(".ui"):
                get_path_file = os.path.split(paths)
                folder_path = get_path_file[0]
                folder.append(folder_path)
                folder_name = os.path.basename(folder_path)
                file_name = get_path_file[1]
                get_basename = os.path.basename(self.get_current_dir())
                self.name = get_basename.join(".*")
                self.extension = '{}/{}'.format(folder_path, file_name)
                try:
                    setup(
                        ext_modules=cythonize(
                            [
                                Extension(self.name, [self.extension],

                                          ),

                            ],
                            build_dir="build",
                            compiler_directives=dict(
                                always_allow_keywords=True
                            )),

                    )
                except:
                    pass

        self.copy_pyd_files()

    def copy_pyd_files(self):
        for root, dirs, files in os.walk(self.get_current_dir()):
            for file in files:
                if not os.path.isdir("build") and not os.path.isdir("compiled_pyd_files"):
                    files_list.append(os.path.join(root, file))

        for files in files_list:
            get_path = os.path.split(files)
            self.get_head = get_path[0]
            get_current_path = self.get_compiled_dir()
            self.files_copy_func(get_current_path, self.get_head)

        self.files_copy_func(self.get_compiled_dir(), self.get_current_dir())

    def get_compiled_dir(self):
        get_current_path = os.path.join(self.get_current_dir(), "compiled_pyd_files")
        return get_current_path

    @staticmethod
    def files_copy_func(source, destination):
        copy_files = distutils.dir_util.copy_tree(source, destination)
        return copy_files


if __name__ == "__main__":
    compile()
