import os
import pathlib

data_path_name = 'data'
log_path_name = 'log'


def gen_current_path(path_name, filename):
    cwd = pathlib.Path.cwd()
    data_path = os.path.join(cwd, path_name)
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    file_path = os.path.join(data_path, filename)
    return file_path


log_path = gen_current_path('log', 'output.log')
