import os
import json


def list_directory(directory_path):
    """
    Lists the contents of the specified directory.

    :param directory_path: Path to the directory to be listed.
    :return: A JSON object with the list of files and directories.
    """
    try:
        # List directory contents
        directory_contents = os.listdir(directory_path)
        return json.dumps({"success": True, "contents": directory_contents})
    except FileNotFoundError:
        return json.dumps({"success": False, "error": "Directory not found"})
    except OSError as e:
        return json.dumps(
            {"success": False, "error": f"Error accessing directory: {e}"}
        )
