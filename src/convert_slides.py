import os
import comtypes.client
from pathlib import Path

def convert_pptx_to_pdf():
    # 1. Define paths (relative to where the script is run)
    base_dir = Path("resources/presentations").resolve()
    pdf_dir = base_dir / "pdfs"
    
    # 2. Create the pdfs subfolder if it doesn't exist
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # 3. Initialize PowerPoint COM object
    print("Opening Microsoft PowerPoint...")
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    # 32 is the format code for PDF export in PowerPoint
    PDF_FORMAT = 32 

    try:
        # 4. Find all .pptx files in the directory
        for pptx_file in base_dir.glob("*.pptx"):
            # Ignore temporary files that start with ~$
            if pptx_file.name.startswith("~$"):
                continue

            pdf_file = pdf_dir / f"{pptx_file.stem}.pdf"

            # 5. Skip conversion if the PDF already exists and is up to date
            if pdf_file.exists() and pdf_file.stat().st_mtime >= pptx_file.stat().st_mtime:
                print(f"Skipping {pptx_file.name} (PDF is already up to date).")
                continue

            print(f"Converting {pptx_file.name} to PDF...")
            
            # Open presentation, save as PDF, and close
            presentation = powerpoint.Presentations.Open(str(pptx_file), WithWindow=False)
            presentation.SaveAs(str(pdf_file), PDF_FORMAT)
            presentation.Close()
            
            print(f"Successfully created {pdf_file.name}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # 6. Ensure PowerPoint closes cleanly in the background
        powerpoint.Quit()
        print("Conversion complete.")

if __name__ == "__main__":
    convert_pptx_to_pdf()