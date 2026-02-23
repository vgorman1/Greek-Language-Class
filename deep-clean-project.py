# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 13:47:19 2026

@author: rgorm
"""
import os
import re

# This regex finds the Jekyll prolog (--- blocks)
prolog_pattern = re.compile(r"^---.*?---\n+", re.DOTALL)

def clean_name(name):
    """Lowercase, replaces underscores/spaces with hyphens, removes doubles."""
    new_name = name.lower().strip().replace("_", "-").replace(" ", "-")
    while "--" in new_name:
        new_name = new_name.replace("--", "-")
    return new_name

def deep_process():
    # Walk through every folder in the repo
    for root, dirs, files in os.walk(".", topdown=False):
        
        # Safety: skip git data
        if '.git' in root:
            continue

        # A. Process Files (Renaming and Prolog Stripping)
        for file in files:
            old_path = os.path.join(root, file)
            
            # 1. Strip Prologs from HTML files to unlock Oxygen Author Mode
            if file.endswith(".html"):
                try:
                    with open(old_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if content.startswith("---"):
                        new_content = prolog_pattern.sub("", content)
                        with open(old_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Prolog stripped: {old_path}")
                except Exception as e:
                    print(f"Could not process {file}: {e}")

            # 2. Rename the file (Casing, Underscores, Spaces)
            new_filename = clean_name(file)
            if new_filename != file:
                new_path = os.path.join(root, new_filename)
                # Check if file exists to avoid collision
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renamed File: {file} -> {new_filename}")

        # B. Rename Directories
        for d in dirs:
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
    deep_process()
    print("\nDeep clean complete. All files are standardized.")