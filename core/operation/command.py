import os, sys
import shutil, fileinput

class Command():
    def delete_folder(self, name):
        self.name = name

        for root, dirs, files in os.walk(self.name):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def create_folder(self, name):
        self.name = name

        if not os.path.exists(self.name):
            os.mkdir(self.name)

    def recursive_copy(self, src, dest):
        self.src = src
        self.dest = dest

        shutil.copytree(src, dest, dirs_exist_ok=True)

    def file_copy(self, src, dest):
        self.src = src
        self.dest = dest

        try:
            shutil.copy(self.src, self.dest)
            print("File copied successfully.")
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

    def replacement(self, file, previousw, nextw):
        self.file = file
        self.previousw = previousw
        self.nextw = nextw
        
        for line in fileinput.input(self.file, inplace=1):
            line = line.replace(self.previousw, self.nextw)
            sys.stdout.write(line)

    def convert_to_list(self, string):
        self.string = string

        list_result = list(string.split(" "))
        return list_result

    def clear(self):
        os.system("clear")