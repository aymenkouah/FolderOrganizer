#Made by: Kouah Mohammed Aymen
#Computer science student at "National Computer science Engineering School, Algiers (ESI)"
#E-mail: jm_kouah@esi.dz
#Github: https://github.com/aymenkouah

#Requires installaling "filetype"
#https://pypi.org/project/filetype/


# Modules
import os
import filetype
import random
import shutil


# Classes

class file():
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path)
        self.type = filetype.guess(path)
        try:
            self.extension = self.type.extension
            self.mime = self.type.mime
        except:
            self.extension = "Other"
            self.mime = "Other"

    def __repr__(self):
        return os.path.basename(self.path)


class folder():
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.files_entries = [entry for entry in os.scandir(
            self.path) if entry.is_file()]
        self.files_paths = [entry.path for entry in self.files_entries]
        self.files_names = [entry.name for entry in self.files_entries]

    def __repr__(self):
        return os.path.basename(self.path)

    def organize_by_type(self):
        for entry in self.files_paths:
            new_file = file(entry)
            dest = self.path + '/' + new_file.mime
            if not os.path.exists(dest):
                os.makedirs(dest)
            os.rename(entry, dest + '/' + new_file.name)

    def just_files(self, dest):
        for entry in os.scandir(self.path):
            if entry.is_dir():
                new_fol = folder(entry.path)
                new_fol.just_files(dest)
            else:
                new = dest + '\\' + entry.name
                new = self.new_name(new)
                os.rename(entry.path, new)

    def new_name(self, new):
        while os.path.exists(new) and os.path.isfile(new):
            i = len(new)-1
            while (new[i] != '.') and i > 0:
                i = i - 1
            if i == 0:
                i = len(new)

            new = new[0:i] + str(random.randint(0, 10000)) + '-' + new[i:]
        return new


# Variables

Path = input("Enter the path of the directory: ")
target = folder(
    r"%s" % Path)


# Functions

def organize(fol):
    to_organize = fol.path + '/../to_organize'
    new_fol = fol.name
    os.mkdir(to_organize)
    fol.just_files(to_organize)

    org = folder(to_organize)
    org.organize_by_type()

    os.chdir(fol.path+'/..')

    shutil.rmtree(fol.path)

    os.rename(os.path.basename(to_organize), new_fol)


# Main Code
if __name__ == '__main__':
    organize(target)
    input("Done")
