# Build a tests file for the get_files_info function
import os
import unittest
# import get_files_info function
from functions.get_files_info import get_files_info
from functions.get_files_info import get_file_content
from functions.get_files_info import write_file
from functions.run_python import run_python_file

working_directory = os.getcwd()

print(get_file_content(working_directory, 'main.py'))
print(write_file(working_directory, 'main.txt', 'hello'))
print(run_python_file(working_directory, 'main.py'))
print(get_files_info(working_directory, 'pkg'))