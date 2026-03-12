import os
from pathlib import Path

def dry_run_pptx_to_pdf():
    # 1. Define paths exactly as they are in the live script
    base_dir = (Path(__file__).parent.parent / "resources" / "presentations").resolve()
    pdf_dir = base_dir / "pdfs"
    
    print("--- STARTING DRY RUN ---\n")
    print(f"🔍 Looking for presentations in: {base_dir}")
    print(f"📁 Would save PDFs to:         {pdf_dir}\n")
    
    # Verify the target directory actually exists
    if not base_dir.exists():
        print(f"❌ ERROR: The directory does not exist! Please check your folder structure.")
        return

    # Find all .pptx files
    pptx_files = list(base_dir.glob("*.pptx"))
    
    if not pptx_files:
        print("⚠️ No .pptx files found in the target directory.")
        return

    # Process findings
    for pptx_file in pptx_files:
        # Ignore temporary PowerPoint files that start with ~$
        if pptx_file.name.startswith("~$"):
            print(f"👻 [IGNORE]  Would ignore temporary file: {pptx_file.name}")
            continue

        pdf_file = pdf_dir / f"{pptx_file.stem}.pdf"

        # Check the logic for skipping vs converting
        if pdf_file.exists() and pdf_file.stat().st_mtime >= pptx_file.stat().st_mtime:
            print(f"⏭️  [SKIP]    {pptx_file.name} (PDF already exists and is up to date)")
        else:
            print(f"✅ [CONVERT] {pptx_file.name}")
            print(f"             -> Would save as: {pdf_file.name}")

    print("\n--- DRY RUN COMPLETE ---")
    print("Zero files were created, modified, or opened.")

if __name__ == "__main__":
    dry_run_pptx_to_pdf()