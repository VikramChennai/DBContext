import asyncio
import tempfile
import os
import docker

async def run_command(container, command: str):
    """
    Executes a command in the Docker container.

    Args:
        container: The Docker container object.
        command (str): The command to execute.

    Returns:
        str: The output of the command execution.
    """
    cmd = ['/bin/sh', '-c', command]
    exec_id = container.exec_run(cmd=cmd)
    output = exec_id.output.decode('utf-8').strip()
    return output

async def write_file(container, file_path: str, content: str):
    """
    Writes content to a file in the Docker container.

    Args:
        container: The Docker container object.
        file_path (str): The path to the file in the container.
        content (str): The content to write to the file.

    Returns:
        str: The content of the created file.
    """
    escaped_content = content.replace("'", "'\\''")
    await run_command(container, f"echo '{escaped_content}' > {file_path}")
    result = await run_command(container, f"cat {file_path}")
    return result

async def execute_script(container, script_content: str):
    """
    Executes a Python script passed as a string in the Docker container.

    Args:
        container: The Docker container object.
        script_content (str): The content of the Python script to execute.

    Returns:
        str: The output of the script execution.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(script_content)
        temp_file_path = temp_file.name

    try:
        await write_file(container, temp_file_path, script_content)
        result = await run_command(container, f"python {temp_file_path}")
        return result
    finally:
        os.unlink(temp_file_path)

async def create_and_execute_file(container, file_path: str, file_name: str, content: str):
    """
    Creates a file with the given content and executes it in the Docker container.

    Args:
        container: The Docker container object.
        file_path (str): The path to create the file. '' represents the current directory.
        file_name (str): The name of the file to create.
        content (str): The content to write to the file.

    Returns:
        str: The output of the script execution.
    """
    full_file_path = os.path.join(file_path, file_name) if file_path else file_name
    await write_file(container, full_file_path, content)
    result = await run_command(container, f"python {full_file_path}")
    return result
