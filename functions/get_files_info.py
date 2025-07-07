import os
import json
import google
from google.generativeai import types
from config import system_prompt



def get_files_info(working_directory, directory=None):
	# if directory is None, default to listing the working directory itself
	if directory is None:
		directory = working_directory

	# use os.path.join() to ensure the directory is relative to the working directory
	directory = os.path.join(working_directory, directory)
	
	# Ensure the working directory and directory are absolute paths
	parent_dir = os.path.abspath(working_directory)
	child_dir = os.path.abspath(directory)

		# Add these debug lines temporarily:
	#print(f"Debug: parent_dir = {parent_dir}")
	#print(f"Debug: child_dir = {child_dir}")
	#print(f"Debug: working_directory = {working_directory}")
	#print(f"Debug: directory = {directory}")


	# Make sure both paths end with a path separator
	#parent_dir = os.path.join(parent_dir, '')
	#child_dir = os.path.join(child_dir, '')
	
		# Check if child_dir is within parent_dir using os.path.commonpath
	try:
		common = os.path.commonpath([parent_dir, child_dir])
		if common != parent_dir:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	except ValueError:
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	
	if not os.path.isdir(directory):
		return f'Error: "{directory}" is not a directory'

	try:
		# Build and return a string of the contents of the directory
		files = os.listdir(directory)
		files_info = []
		# Determine file size and whether it is a directory or file
		for file in files:
			file_path = os.path.join(directory, file)
			file_size = os.path.getsize(file_path)
			if os.path.isdir(file_path):
				files_info.append(f"- {file}: file_size={file_size} bytes, is_dir={os.path.isdir(file_path)}")
			else:
				files_info.append(f"- {file}: file_size={file_size} bytes, is_dir={os.path.isdir(file_path)}")
		
		# Combine the file information into a single string
		files_info_str = "\n".join(files_info)
		
			# Return the formatted string in this format: - <name>: file_size=<size> bytes, is_dir=<True/False>
		return files_info_str

	except Exception as e:
		return f'Error: {e}'
	
# Create function to get file content
def get_file_content(working_directory, file_path):

	abs_path = os.path.join(working_directory, file_path)

	# Ensure the working directory and directory are absolute paths
	working_dir = os.path.abspath(working_directory)
	file_path_dir = os.path.abspath(abs_path)

	# Check if file_path is within working_directory using os.path.commonpath
	try:
		common = os.path.commonpath([working_dir, file_path_dir])
		if common != working_dir:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	except ValueError:
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	
	
	
	# if file_path is not a file, return an error message
	if not os.path.isfile(abs_path):
		return f'Error: File not found or is not a regular file: "{file_path}"'
	
	# read the file and return its content as string. Always return. if file is longer than 1000 characters, truncate it to 1000 characters and append message
	try:
		with open(abs_path, 'r') as file:
			content = file.read()
			if len(content) > 10000:
				return f"{content[:10000]}[...File \"{file_path}\" truncated at 10000 characters]"
			return content
	except Exception as e:
		return f'Error: {e}'

# Write and overwrite files
def write_file(working_directory, file_path, content):
	abs_path = os.path.join(working_directory, file_path)

	# Ensure the working directory and directory are absolute paths
	working_dir = os.path.abspath(working_directory)
	file_path_dir = os.path.abspath(abs_path)

	# Check if file_path is within working_directory using os.path.commonpath
	try:
		common = os.path.commonpath([working_dir, file_path_dir])
		if common != working_dir:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	except ValueError:
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	
	# if file_path doesn't exist, create it. If there is an error, return an error message
	if not os.path.exists(os.path.dirname(abs_path)):
		try:
			os.makedirs(os.path.dirname(abs_path))
		except Exception as e:
			return f'Error: Could not create directory for "{file_path}": {e}'

	# write the content to the file, overwriting it if it exists
	try:
		with open(abs_path, 'w') as file:
			file.write(content)
		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f'Error: Could not write to file "{file_path}": {e}'
	

# Use types.FunctionDeclaration to build teh "declaration" or "schema" of the function
schema_get_files_info = types.protos.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.protos.Schema(
        type=types.protos.Type.OBJECT,
        properties={
            "directory": types.protos.Schema(
                type=types.protos.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.protos.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)


# If/else to check response.candidates and handle function calls
def handle_function_calls(response):
	for candidate in response.candidates:
		for part in candidate.content.parts:
			if hasattr(part, "function_call") and part.function_call:
				args = dict(part.function_call.args)  # convert to regular dict
				print(f"Calling function: {part.function_call.name}({args})")
			elif hasattr(part, "text") and part.text:
				print(part.text)
		
		
	


