# Build a tests file for the get_files_info function
import os
import unittest
# import get_files_info function
from functions.get_files_info import get_files_info
from functions.get_files_info import get_file_content
from functions.get_files_info import write_file, handle_function_calls, available_functions, call_function
from functions.run_python import run_python_file

working_directory = os.getcwd()

print(call_function( 'get_files_info','test.txt'))