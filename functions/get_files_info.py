import os

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