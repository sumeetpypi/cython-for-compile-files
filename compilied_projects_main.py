import fnmatch
import glob

from Qt import QtWidgets, QtGui
from Qt import QtCompat
from Qt import QtCore
import sys
import distutils.dir_util
import shutil
import os
import tempfile
from fnmatch import fnmatch
import customDarkPalette

project_name = []
old_files = dict()
saving_old_files = []
clean = []
path_1 = []


class DropWidget(QtWidgets.QListWidget):
    files_dropped = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(DropWidget, self).__init__(parent)
        self._initialize()

    def _initialize(self):
        self.setAcceptDrops(True)
        self.setMinimumHeight(50)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            files_to_append = []
            for url in event.mimeData().urls():
                file_path = str(url.toLocalFile())
                files_to_append.append(file_path)

            if not files_to_append:
                event.ignore()

            event.accept()
            self.files_dropped.emit(files_to_append)
        else:
            event.ignore()


class compliled_project(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(compliled_project, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), 'complied_projects.ui')
        self.ui = QtCompat.loadUi(ui_file, self)
        self.setWindowTitle('Compiled projects')

        self.drop_widget = DropWidget()
        self.ui.verticalLayout_2.addWidget(self.drop_widget)
        self.ui_connections()

    def ui_connections(self):
        self.drop_widget.files_dropped.connect(self.drag_drop_files)
        self.ui.browse.clicked.connect(self.compilation_location)
        # self.ui.compile_projects.clicked.connect(self.compilation_button)
        self.ui.compile_projects.clicked.connect(self.compilation_button)

    @staticmethod
    def get_temp_path():
        # temp_dir = os.path.dirname("C:\Users\duggs\Downloads")
        temp_dir = tempfile.gettempdir()
        return temp_dir

    def drag_drop_files(self, file):
        for self.files in file:
            self.drop_widget.addItem(self.files)
        count = self.drop_widget.count()
        for index in range(count):
            self.items = self.drop_widget.item(index).text()
        for folders in os.listdir(self.items):
            if folders.endswith('git') and folders.endswith('idea'):
                delete_folders = os.path.join(self.items, folders)
                shutil.rmtree(delete_folders)

        self.get_project_name = os.path.basename(self.items)
        temp_path = self.get_temp_path()
        self.create_dir_in_temp = os.path.join(temp_path, self.get_project_name)
        if os.path.exists(self.create_dir_in_temp):
            shutil.rmtree(self.create_dir_in_temp)

        self.make_dir(self.create_dir_in_temp)
        self.files_copy_func(self.items, self.create_dir_in_temp)

        for root, dir, file in os.walk(self.create_dir_in_temp):
            for file in file:
                if fnmatch(file, '*__init__.py'):
                    os.remove(os.path.join(root, file))
                if fnmatch(file, '*.pyc'):
                    os.remove(os.path.join(root, file))

        setup_file = os.path.dirname(__file__)
        get_file = os.path.join(setup_file, 'setup.py')
        fle = os.path.basename(get_file)
        cmd_file = os.path.join(setup_file, 'cmd.py')
        fle_cmd = os.path.basename(cmd_file)

        self.build_folder_path = os.path.join(self.create_dir_in_temp, self.get_project_name)
        os.mkdir(self.build_folder_path)
        get_build_file = os.path.join(self.create_dir_in_temp, self.get_project_name)
        shutil.copy(fle, get_build_file)
        shutil.copy(fle_cmd, get_build_file)
        self.files_copy_func(self.create_dir_in_temp, self.build_folder_path)
        self.build_folder_path = os.path.join(self.create_dir_in_temp, self.get_project_name)
        mydir_tmp = self.build_folder_path
        os.chdir(mydir_tmp)
        self.current_dir = os.getcwd()
        self.saving_old_files()

    def compilation_button(self):
        self.get_subprocess()
        self.delete_unwanted_files()
        self.final_output_dir_compilation()
        self.delete_py_files()

    def get_current_dir(self):
        current_dir = os.getcwd()
        return current_dir

    @staticmethod
    def get_subprocess():
        import subprocess
        subprocess.call(["python", "cmd.py"])

    def saving_old_files(self):
        current_dir = self.get_current_dir()
        for root, dir, files in os.walk(current_dir):
            for folders in files:
                old_file = os.path.join(root, folders)
                file_names = os.path.splitext(old_file)[0]
                saving_old_files.append(file_names)

    @staticmethod
    def make_dir(dir):
        os.mkdir(dir)

    @staticmethod
    def files_copy_func(source, destination):
        copy_files = distutils.dir_util.copy_tree(source, destination)
        return copy_files

    def temp_dir(self):
        temp_path = self.get_temp_path()
        create_dir_in_temp = os.path.join(temp_path, self.get_project_name)
        os.mkdir(create_dir_in_temp)
        return create_dir_in_temp

    def delete_unwanted_files(self):
        for files in saving_old_files:
            old_files = "{}.*".format(files)
            self.cleanupFiles = glob.glob(old_files)
            for cleanupFile in self.cleanupFiles:
                clean.append(cleanupFile)
            current_dir = self.get_current_dir()
            exclude = ["build"]
            for root, dir, files in os.walk(current_dir):
                remove_build = [dir.remove(d) for d in list(dir) if d in exclude]
                for folders in files:
                    old_file = os.path.join(root, folders)
                    path_1.append(old_file)

        self.replicaations_clean = list(set(clean))
        self.replication_new = list(set(path_1))
        self.get_item = [items for items in self.replication_new if
                         items not in self.replicaations_clean]
        for self.dl in self.get_item:
            os.remove(self.dl)

        self.unwanted_folders_and_files()


    def unwanted_folders_and_files(self):
        count = self.drop_widget.count()
        for index in range(count):
            self.items = self.drop_widget.item(index).text()
        get_project_name = os.path.basename(self.items)

        folders_names = [get_project_name]
        for folders in folders_names:
            shutil.rmtree(folders)

    def copy_original_project(self):
        count = self.drop_widget.count()
        for index in range(count):
            self.items = self.drop_widget.item(index).text()
        get_project_name = os.path.basename(self.items)
        temp_path = self.get_temp_path()
        create_dir_in_temp = os.path.join(temp_path, get_project_name)
        self.build_dir_path = os.path.join(create_dir_in_temp, "build")
        self.files_copy_func(self.items, self.build_dir_path)

    def compilation_location(self):
        self.selected_dir = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Choose Directory',
                                                                       directory=os.getcwd())
        self.output_dir_name = self.ui.output_line_edit.setText(self.selected_dir)

    def final_output_dir_compilation(self):
        count = self.drop_widget.count()
        for index in range(count):
            self.items = self.drop_widget.item(index).text()
        get_project_name = os.path.basename(self.items)
        temp_path = self.get_temp_path()
        create_dir_in_temp = os.path.join(temp_path, get_project_name)
        build_dir_path = os.path.join(create_dir_in_temp, get_project_name)
        get_project_path = os.path.join(self.selected_dir, get_project_name)
        self.make_dir(get_project_path)
        self.files_copy_func(build_dir_path, get_project_path)

    def delete_py_files(self):
        for root, dir, file in os.walk(self.selected_dir):
            for file in file:
                if fnmatch(file, '*.py'):
                    os.remove(os.path.join(root, file))
                if fnmatch(file, '*.c'):
                    os.remove(os.path.join(root, file))
                # if fnmatch(file, '*.ui'):
                #     os.remove(os.path.join(root, file))


if __name__ == '__main__':
    compliled_projects = QtWidgets.QApplication(sys.argv)
    # customDarkPalette.customDarkPalette(compliled_projects)
    app = compliled_project()
    app.show()
    sys.exit(compliled_projects.exec_())
