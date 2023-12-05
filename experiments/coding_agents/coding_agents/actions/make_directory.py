import json
import os

def make_directory(directory_path):
    """
    Creates a directory at the specified path, handling any depth of directories.
    Returns a JSON string indicating the success or failure of the operation.

    :param directory_path: A string specifying the path of the directory to be created.
    :return: A JSON string with the operation result.
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return json.dumps({"success": True, "message": f"Directory '{directory_path}' created successfully."})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
