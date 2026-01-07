import os
import re

def get_solution_files():
    """Gets all Python solution files from the 'solutions' directory."""
    solutions_dir = 'solutions'
    if not os.path.exists(solutions_dir):
        return []
    return sorted([f for f in os.listdir(solutions_dir) if f.endswith('.py')])

def title_case_from_slug(slug):
    """Converts a slug-like-string to Title Case."""
    return ' '.join(word.capitalize() for word in slug.split('-'))

def parse_solution_file(filename):
    """Parses metadata from a solution file (comments or docstring)."""
    match = re.match(r'(\d+)\.(.+)\.py', filename)
    if not match:
        return None
    
    number, slug = match.groups()
    metadata = {
        'no': int(number),
        'slug': slug,
        'title': title_case_from_slug(slug),
        'difficulty': 'N/A',
        'topics': 'N/A',
        'acceptance': 'N/A',
        'filename': filename
    }

    file_path = os.path.join('solutions', filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    docstring_match = re.search(r'^[\s]*[\'"]{3}([\s\S]*?)[\'"]{3}', content)
    if docstring_match:
        doc_content = docstring_match.group(1)
        for line in doc_content.split('\n'):
            if 'Topics:' in line:
                metadata['topics'] = line.split('Topics:', 1)[1].strip()
            elif 'Category:' in line: # Handle old format
                metadata['topics'] = line.split('Category:', 1)[1].strip()
            elif 'Difficulty:' in line:
                metadata['difficulty'] = line.split('Difficulty:', 1)[1].strip()
            elif 'Acceptance:' in line:
                metadata['acceptance'] = line.split('Acceptance:', 1)[1].strip()
    
    return metadata

def generate_problem_index(solutions_metadata):
    """Generates the Markdown table for the problem index."""
    header = "## Index\n\n"
    table_header = """| # | Title | Difficulty | Topics | Solution |
|---|---|---|---|---|
"""
    
    table_rows = []
    for meta in solutions_metadata:
        solution_path = f"./solutions/{meta['filename']}"
        # Use the 'topics' key for the table.
        row = f"| {meta['no']} | {meta['title']} | {meta['difficulty']} | {meta['topics']} | [Python]({solution_path}) |"
        table_rows.append(row)
    
    return header + table_header + "\n".join(table_rows)

def generate_tree_diagram():
    """Generates a directory tree diagram with annotations, similar to leetcode-rs."""
    items = [
        ('solutions', 'Python solutions (source of truth)', True),
        ('scripts',   'Automation scripts', True),
        ('.gitignore', None, False),
        ('README.md',  None, False)
    ]
    tree_lines = ["letkod/"]
    existing_items = []
    for name, desc, is_dir in items:
        if os.path.exists(name):
            display_name = f"{name}/" if is_dir else name
            existing_items.append((display_name, desc))
    count = len(existing_items)
    for i, (name, desc) in enumerate(existing_items):
        is_last = (i == count - 1)
        prefix = "└── " if is_last else "├── "
        line = f"{prefix}{name}"
        if desc:
            line = f"{line:<22}# {desc}"
        tree_lines.append(line)
    return "## Repository Structure\n\n```text\n" + "\n".join(tree_lines) + "\n```"

def generate_usage_section():
    return "## Usage\n\n1.  **Clone the repository:**\n    ```bash\n    git clone https://github.com/kaylaradf/letkod.git\n    cd letkod\n    ```\n2.  **Navigate to a solution:**\n    ```bash\n    cd solutions\n    ```\n3.  **Run a solution (example):**\n    ```bash\n    python 1.two-sum.py\n    ```\n"

def main():
    print("Starting README update process...")
    solution_files = get_solution_files()
    solutions_metadata = []
    for filename in solution_files:
        meta = parse_solution_file(filename)
        if meta:
            solutions_metadata.append(meta)
    solutions_metadata.sort(key=lambda x: x['no'])
    new_index = generate_problem_index(solutions_metadata)
    new_tree = generate_tree_diagram()
    new_usage = generate_usage_section()
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = "# Letkod\n\n"
    intro_match = re.search(r'(^[​‌‍‎‏﻿\]*?)(?=## Index)', content, re.MULTILINE)
    intro = intro_match.group(1) if intro_match else "# Letkod\n\n"
    solved_count = len(solutions_metadata)
    intro = re.sub(
        r'!\\[Progress\\]\(https://img\.shields\.io/badge/progress-.*?%2F(\d+)-brightgreen\.svg\)',
        f'!\\[Progress\\]\(https://img.shields.io/badge/progress-{solved_count}%2F\\1-brightgreen.svg)',
        intro
    )
    proj_struct_match = re.search(r'(## Project Structure[\s\S]*?)(?=## Usage)', content, re.MULTILINE)
    if proj_struct_match:
        project_structure = proj_struct_match.group(1)
    else:
        project_structure = "## Project Structure\n\n"
    notes_match = re.search(r'(## Notes[\s\S]*$)', content, re.MULTILINE)
    notes = notes_match.group(1) if notes_match else "## Notes\n\n"
    final_content = f"{intro}{new_index}\n\n{new_tree}\n\n{project_structure}\n\n{new_usage}\n\n{notes}"
    final_content = re.sub(r'\n{3,}', '\n\n', final_content)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("README.md has been successfully updated while preserving your edits.")

if __name__ == '__main__':
    main()
