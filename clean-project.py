# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 13:47:19 2026

@author: rgorm
"""

import os
import re

prolog_pattern = re.compile(r"^---.*?---\n+", re.DOTALL)

def clean_name(name):
    """Lowercase, replace spaces with hyphens, remove double hyphens."""
    new_name = name.lower().strip().replace(" ", "-")
    while "--" in new_name:
        new_name = new_name.replace("--", "-")
    return new_name

def process_files():
    # Walking through EVERYTHING starting from the current directory
    for root, dirs, files in os.walk(".", topdown=False):
        
        # 1. SAFETY: Skip the .git folder and the src folder
        if '.git' in root or 'src' in root:
            continue

        # A. Process Files
        for file in files:
            # Only touch HTML files
            if file.endswith(".html"):
                old_path = os.path.join(root, file)
                
                # Strip the Prolog
                with open(old_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if content.startswith("---"):
                    new_content = prolog_pattern.sub("", content)
                    with open(old_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Prolog stripped: {old_path}")

                # Rename the file
                new_filename = clean_name(file)
                if new_filename != file:
                    new_path = os.path.join(root, new_filename)
                    os.rename(old_path, new_path)
                    print(f"Renamed File: {file} -> {new_filename}")

        # B. Rename Directories
        for d in dirs:
            # Don't rename .git or src
            if d == '.git' or d == 'src':
                continue
                
            old_dir_path = os.path.join(root, d)
            new_dir_name = clean_name(d)
            if new_dir_name != d:
                new_dir_path = os.path.join(root, new_dir_name)
                if not os.path.exists(new_dir_path):
                    os.rename(old_dir_path, new_dir_path)
                    print(f"Renamed Folder: {d} -> {new_dir_name}")

if __name__ == "__main__":
    process_files()
    print("\nDone! Check your files in Oxygen now.")