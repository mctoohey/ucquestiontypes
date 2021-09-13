import os
from shutil import copyfile

QUESTION_TYPE_TEMPLATES_DIR = "question_type_templates"
QUESTION_TYPE_BUILDS_DIR = "question_type_builds"


def copy_dir(src, dest):
    for file_name in os.listdir(src):
        copyfile(os.path.join(src, file_name), os.path.join(dest, file_name))


def build_question_type(path, name):
    dest = os.path.join(QUESTION_TYPE_BUILDS_DIR, name)
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    files = os.listdir(path)
  
    if 'template.py' not in files:
        print("Error: question type must include a 'template.py' file")
        return
    
    for file_name in files:
        if file_name != 'include':
            copyfile(os.path.join(path, file_name), os.path.join(dest, file_name))

    if 'include' in files:
        with open(os.path.join(path, 'include')) as include_file:
            include_locations = include_file.read().splitlines()
            for location in include_locations:
                path = os.path.join("src", location)
                if os.path.isfile(path):
                    copyfile(path, os.path.join(dest, location))
                else:
                    copy_dir(path, dest)



def main():
    cwd = os.getcwd()
    question_type_dirs = os.listdir(QUESTION_TYPE_TEMPLATES_DIR)
    for dir in question_type_dirs:
        assert not os.path.isfile(dir)
        build_question_type(os.path.join(QUESTION_TYPE_TEMPLATES_DIR, dir), dir)
        




if __name__ == "__main__":
    main()
