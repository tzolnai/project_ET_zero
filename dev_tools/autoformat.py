import os


def format_files_in_directory(dir_path):
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path) and file_path.endswith(".py"):
            print("Formating file: " + file_path)
            os.system("autopep8 -i --ignore E402 --max-line-length 100 " + file_path)
        elif os.path.isdir(file_path) and not file_path.endswith("externals"):
            print("Stepping into directory: " + file_path)
            format_files_in_directory(file_path)


this_path = os.path.split(os.path.abspath(__file__))[0]
root_path = os.path.split(this_path)[0]
format_files_in_directory(root_path)
