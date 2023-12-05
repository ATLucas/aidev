import json

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return json.dumps({"success": True, "content": content})
    except FileNotFoundError:
        return json.dumps({"success": False, "error": "File not found"})
    except IOError:
        return json.dumps({"success": False, "error": "Error reading file"})
