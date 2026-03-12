import os
import comtypes.client
import logging
from pathlib import Path

def convert_pptx_to_pdf():
    # 1. Define paths
    base_dir = (Path(__file__).parent.parent / "resources" / "presentations").resolve()
    pdf_dir = base_dir / "pdfs"
    
    # 2. Create the pdfs subfolder if it doesn't exist
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # 3. Set up the log file
    log_file = base_dir / "conversion_log.txt"
    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    print(f"Starting conversion. A detailed log will be saved to: {log_file.name}")
    logging.info("--- STARTED BATCH CONVERSION ---")

    # 4. Initialize PowerPoint COM object
    print("Opening Microsoft PowerPoint in the background...")
    try:
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        PDF_FORMAT = 32 
        
        pptx_files = list(base_dir.glob("*.pptx"))
        converted_count = 0
        skipped_count = 0

        # 5. Process files
        for pptx_file in pptx_files:
            if pptx_file.name.startswith("~$"):
                continue

            pdf_file = pdf_dir / f"{pptx_file.stem}.pdf"

            if pdf_file.exists() and pdf_file.stat().st_mtime >= pptx_file.stat().st_mtime:
                print(f"Skipping {pptx_file.name} (Up to date)")
                logging.info(f"SKIPPED: {pptx_file.name} (PDF already up to date)")
                skipped_count += 1
                continue

            print(f"Converting: {pptx_file.name}...")
            
            # Open presentation, save as PDF, and close
            presentation = powerpoint.Presentations.Open(str(pptx_file), WithWindow=False)
            presentation.SaveAs(str(pdf_file), PDF_FORMAT)
            presentation.Close()
            
            logging.info(f"SUCCESS: Converted {pptx_file.name}")
            converted_count += 1

        logging.info(f"--- FINISHED: {converted_count} converted, {skipped_count} skipped ---")
        print(f"\nDone! Converted {converted_count} files. Skipped {skipped_count} files.")

    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(error_msg)
        logging.error(error_msg)
    
    finally:
        # 6. Ensure PowerPoint closes cleanly
        if 'powerpoint' in locals():
            powerpoint.Quit()
            print("Closed PowerPoint.")

if __name__ == "__main__":
    convert_pptx_to_pdf()