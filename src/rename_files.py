import os

# --- CONFIGURATION ---

# 1. Dynamically find the project root.
# Assuming this script is in: .../Greek-Language-Class/src/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

# 2. Target ONLY the assignments directory.
# This resolves to: .../Greek-Language-Class/resources/assignments
TARGET_DIRS = [
    os.path.join(PROJECT_ROOT, 'resources', 'assignments')
]

# 3. File extensions to target.
TARGET_EXTENSIONS = ('.html', '.pdf')

# 4. Dry-Run Mode (True = preview, False = execute).
DRY_RUN = False

# --- CORE LOGIC ---

def clean_filename(old_name):
    """Converts to lowercase and replaces underscores with hyphens."""
    base, ext = os.path.splitext(old_name)
    clean_base = base.lower().replace('_', '-')
    return f"{clean_base}{ext}"

def run_cleanup():
    print(f"--- Starting Filename Cleanup (Dry-Run = {DRY_RUN}) ---")
    
    for directory_path in TARGET_DIRS:
        if not os.path.exists(directory_path):
            print(f"Warning: Directory '{directory_path}' not found. Check your folder structure.")
            continue

        print(f"\nScanning: {directory_path}")
        
        # Sort files to ensure consistent processing order
        for old_name in sorted(os.listdir(directory_path)):
            old_file_path = os.path.join(directory_path, old_name)
            
            # Skip folders and non-target file types
            if not os.path.isfile(old_file_path) or not old_name.lower().endswith(TARGET_EXTENSIONS):
                continue
                
            new_name = clean_filename(old_name)
            
            # Skip if already perfectly formatted
            if old_name == new_name:
                continue
                
            new_file_path = os.path.join(directory_path, new_name)
            
            # Prevent accidentally overwriting an existing file
            if os.path.exists(new_file_path):
                print(f"  [SKIPPED - COLLISION]: '{new_name}' already exists.")
                continue
                
            # Execute or preview the rename
            action = "[WOULD RENAME]" if DRY_RUN else "[RENAMED]"
            print(f"  {action}: '{old_name}' -> '{new_name}'")
            
            if not DRY_RUN:
                os.rename(old_file_path, new_file_path)
                
    print("\n--- Cleanup Complete ---")

if __name__ == "__main__":
    run_cleanup()