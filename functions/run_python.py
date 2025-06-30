import os
import subprocess

def run_python_file(working_directory, file_path):
    # if the file_path is outside the working directory, return a string with an error
    abs_path = os.path.join(working_directory, file_path)

    # Ensure the working directory and directory are absolute paths
    working_dir = os.path.abspath(working_directory)
    file_path_dir = os.path.abspath(abs_path)

    # Check if file_path is within working_directory using os.path.commonpath
    try:
        common = os.path.commonpath([working_dir, file_path_dir])
        if common != working_dir:
            return f'STDOUT: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except ValueError:
        return f'STDOUT: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # if the file_path doesn't exist, return a string with an error
    if not os.path.exists(abs_path):
        return f'STDOUT: File "{file_path}" not found.'

    # if the file_path is not a Python file, return a string with an error
    if not file_path.endswith('.py'):
        return f'STDOUT: "{file_path}" is not a Python file.'

    # Use subprocess to run the Python file
    try:
        # set a timeout of 30 seconds to prevent infinite execution
        result = subprocess.run(
            ['python3', file_path],
            cwd=working_directory,
            timeout=30,
            capture_output=True,
            text=True
        )

        # Construct the output message
        output = []
        if result.stdout:
            output.append(f'STDOUT: {result.stdout.strip()}')
        if result.stderr:
            output.append(f'STDERR: {result.stderr.strip()}')
        # if exit code is not 0, return a string with an error including stdout and stderr in message
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        # if the output is empty, return a string with an error
        if not output:
            return 'No output produced'
        else:
            return '\n'.join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
