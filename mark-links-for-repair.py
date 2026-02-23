# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 21:12:54 2026

@author: rgorm
"""
import os
import re

# The directory containing your HTML files
root_dir = "." 

# This regex finds the entire href attribute if it contains sharepoint
# It looks for href="...sharepoint..."
sharepoint_pattern = re.compile(r'href="https://uofnelincoln-my\.sharepoint\.com[^"]*"')
replacement = 'href="/Greek-Language-Class/FIX-ME"'

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(subdir, file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if "sharepoint.com" in content:
                print(f"Cleaning all SharePoint links in: {file_path}")
                # Replace the entire href string with the FIX-ME placeholder
                new_content = sharepoint_pattern.sub(replacement, content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Task complete. All SharePoint links are now: /Greek-Language-Class/FIX-ME")