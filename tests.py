# Build a tests file for the get_files_info function
import os
import unittest
# import get_files_info function
from functions.get_files_info import get_files_info

print(get_files_info('calculator', '.'))
print(get_files_info('calculator', 'pkg'))
print(get_files_info('calculator', '/bin'))
print(get_files_info('calculator', '../'))
