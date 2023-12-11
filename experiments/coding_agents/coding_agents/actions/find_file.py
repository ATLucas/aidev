import os
import json
from glob import glob


def find_file(directory, pattern):
    """
    Searches for files matching a wildcard pattern within a directory and its subdirectories.

    :param directory: The base directory to start the search from.
    :param pattern: The wildcard pattern to search for.
    :return: A JSON object with the paths to the files if found, else an error.
    """
    try:
        # Normalize directory path and append pattern for glob
        search_pattern = os.path.join(os.path.abspath(directory), pattern)

        # Use glob to find files matching the pattern
        matching_files = glob(search_pattern, recursive=True)

        if matching_files:
            return json.dumps({"success": True, "file_paths": matching_files})
        else:
            return json.dumps(
                {"success": False, "error": "No files found matching the pattern"}
            )
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


# Example usage:
# print(find_file('/path/to/search', '*.txt'))
