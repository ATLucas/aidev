import os

def write_js_to_markdown(directory, output_file):
    with open(output_file, 'w') as md_file:
        # Traverse the directory
        for root, dirs, files in os.walk(directory):
            # Skip the node_modules directory
            if 'node_modules' in dirs:
                dirs.remove('node_modules')

            for file in files:
                # Check if the file is a .js file
                if file.endswith('.js'):
                    file_path = os.path.join(root, file)
                    md_file.write('---\n\n')
                    md_file.write(f'{file_path}\n')
                    md_file.write('```\n')
                    with open(file_path, 'r') as js_file:
                        # Write the contents of the .js file to the markdown file
                        md_file.write(js_file.read())
                    md_file.write('\n```\n\n')

# Use the function
write_js_to_markdown('.', 'prompt.md')
