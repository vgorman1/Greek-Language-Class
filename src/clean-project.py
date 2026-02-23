# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 13:47:19 2026

@author: rgorm
"""

import os
import re

# 1. Regex to find the Jekyll prolog (the --- blocks)
# This looks for --- at the very start of the file and catches everything 
# until the next ---, including the newline.
prolog_pattern = re.compile(r"^---.*?---\n+", re.DOTALL)

def clean_name(name):
    """Lowercase, replace spaces with hyphens, remove double hyphens."""
    new_name = name.lower().strip().replace(" ", "-")
    while "--" in new_name:
        new_name = new_name.replace("--", "-")
    return new_name

def process_files():
    # Walk the directory tree from bottom to top
    # (Bottom-up allows us to rename folders without losing the path to files inside)
    for root, dirs, files in os.walk(".", topdown=False):
        
        # A. Process Files
        for file in files:
            if file.endswith(".html"):
                old_path = os.path.join(root, file)
                
                # 1. Strip the Prolog for Oxygen Author Mode
                with open(old_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if content.startswith("---"):
                    new_content = prolog_pattern.sub("", content)
                    with open(old_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Prolog stripped: {file}")

                # 2. Rename the file
                new_filename = clean_name(file)
                if new_filename != file:
                    new_path = os.path.join(root, new_filename)
                    os.rename(old_path, new_path)
                    print(f"Renamed File: {file} -> {new_filename}")

        # B. Rename Directories
        for d in dirs:
            old_dir_path = os.path.join(root, d)
            new_dir_name = clean_name(d)
            if new_dir_name != d:
                new_dir_path = os.path.join(root, new_dir_name)
                # Check if destination exists to avoid overwriting
                if not os.path.exists(new_dir_path):
                    os.rename(old_dir_path, new_dir_path)
                    print(f"Renamed Folder: {d} -> {new_dir_name}")

if __name__ == "__main__":
    process_files()
    print("\nDone! Your files are renamed and prologs are gone.")