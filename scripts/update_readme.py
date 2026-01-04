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
    """Parses metadata from a solution file."""
    match = re.match(r'(\d+)\.(.+)\.py', filename)
    if not match:
        return None
    
    number, slug = match.groups()
    metadata = {
        'no': int(number),
        'slug': slug,
        'title': title_case_from_slug(slug),
        'difficulty': 'N/A',
        'category': 'N/A',
        'filename': filename
    }

    with open(os.path.join('solutions', filename), 'r', encoding='utf-8') as f:
        for line in f:
            line_stripped = line.strip()
            if not line_stripped:
                continue # Skip empty lines

            if line.startswith('# Difficulty:'):
                metadata['difficulty'] = line.split(':', 1)[1].strip()
            elif line.startswith('# Category:'):
                metadata['category'] = line.split(':', 1)[1].strip()
            elif line.startswith('#'):
                continue # Skip other comments
            else:
                # Stop parsing when we hit non-comment, non-empty code
                break
    return metadata

def generate_problem_index(solutions_metadata):
    """Generates the Markdown table for the problem index."""
    header = "## Index\n\n"
    table_header = """| # | Title | Difficulty | Category | Solution |
|---|---|---|---|---|
"""
    
    table_rows = []
    for meta in solutions_metadata:
        solution_path = f"./solutions/{meta['filename']}"
        row = f"| {meta['no']} | {meta['title']} | {meta['difficulty']} | {meta['category']} | [Python]({solution_path}) |"
        table_rows.append(row)
    
    return header + table_header + "\n".join(table_rows)

def generate_tree_diagram():
    """Generates a directory tree diagram with annotations, similar to leetcode-rs."""
    # Define the items we want to display and their descriptions
    # format: (name, description, is_directory)
    items = [
        ('solutions', 'Python solutions (source of truth)', True),
        ('scripts',   'Automation scripts', True),
        ('.gitignore', None, False),
        ('README.md',  None, False)
    ]
    
    tree_lines = ["letkod/"]
    
    # Filter items that actually exist
    existing_items = []
    for name, desc, is_dir in items:
        if os.path.exists(name):
            display_name = f"{name}/" if is_dir else name
            existing_items.append((display_name, desc))
            
    # Build the tree string
    count = len(existing_items)
    for i, (name, desc) in enumerate(existing_items):
        is_last = (i == count - 1)
        prefix = "└── " if is_last else "├── "
        
        line = f"{prefix}{name}"
        if desc:
            # Align comments to a specific column (e.g., 22 characters)
            line = f"{line:<22}# {desc}"
            
        tree_lines.append(line)
            
    return "## Repository Structure\n\n```text\n" + "\n".join(tree_lines) + "\n```"

def generate_usage_section():
    """Generates the standard Usage section."""
    return "## Usage\n\n1.  **Clone the repository:**\n    ```bash\n    git clone https://github.com/kaylaradf/letkod.git\n    cd letkod\n    ```\n2.  **Navigate to a solution:**\n    ```bash\n    cd solutions\n    ```\n3.  **Run a solution (example):**\n    ```bash\n    python 1.two-sum.py\n    ```\n"

def main():
    print("Starting README update process...")
    
    # 1. Parse Solutions
    solution_files = get_solution_files()
    solutions_metadata = []
    for filename in solution_files:
        meta = parse_solution_file(filename)
        if meta:
            solutions_metadata.append(meta)
    solutions_metadata.sort(key=lambda x: x['no'])
    
    # 2. Generate Dynamic Content
    new_index = generate_problem_index(solutions_metadata)
    new_tree = generate_tree_diagram()
    new_usage = generate_usage_section()

    # 3. Read Existing README to preserve specific sections
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = "# Letkod\n\n"

    # Parsing Strategy: Split by Headers
    
    # Intro: Everything before "## Index"
    intro_match = re.search(r'(^[\s\S]*?)(?=## Index)', content, re.MULTILINE)
    intro = intro_match.group(1) if intro_match else "# Letkod\n\n"

    # Project Structure: From "## Project Structure" until "## Usage"
    proj_struct_match = re.search(r'(## Project Structure[\s\S]*?)(?=## Usage)', content, re.MULTILINE)
    if proj_struct_match:
        project_structure = proj_struct_match.group(1)
    else:
        project_structure = "## Project Structure\n\n"

    # Notes: From "## Notes" until End of file
    notes_match = re.search(r'(## Notes[\s\S]*$)', content, re.MULTILINE)
    notes = notes_match.group(1) if notes_match else "## Notes\n\n"

    # 4. Assemble New README
    final_content = f"{intro}{new_index}\n\n{new_tree}\n\n{project_structure}\n\n{new_usage}\n\n{notes}"
    
    # Clean up excessive newlines
    final_content = re.sub(r'\n{3,}', '\n\n', final_content)

    # 5. Write to file
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print("README.md has been successfully updated while preserving your edits.")

if __name__ == '__main__':
    main()