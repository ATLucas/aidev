import json


def write_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
        return json.dumps(
            {"success": True, "message": "Content written to file successfully"}
        )
    except IOError:
        return json.dumps({"success": False, "error": "Error writing to file"})
