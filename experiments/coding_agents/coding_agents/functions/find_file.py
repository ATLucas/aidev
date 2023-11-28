import json
import os

def find_file(directory, file_name):
    for root, dirs, files in os.walk(directory):
        if file_name in files:
            return json.dumps({"success": True, "file_path": os.path.join(root, file_name)})
    return json.dumps({"success": False, "error": "File not found"})
