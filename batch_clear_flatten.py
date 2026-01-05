"""
Batch process all PDFs using clear_then_flatten approach
and save them to a new folder.
"""

import os
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def clear_and_flatten_pdf(input_path: str, output_path: str) -> bool:
    """Clear and flatten a single PDF file."""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Copy pages
        for page in reader.pages:
            writer.add_page(page)

        # Attempt to clear form fields
        fields = reader.get_fields()
        if fields:
            # Update each field value to empty
            # Need to update for each page that has fields
            for page_num, page in enumerate(writer.pages):
                try:
                    writer.update_page_form_field_values(
                        page,
                        {name: "" for name in fields.keys()}
                    )
                except Exception:
                    pass

        # Flatten form fields (best-effort)
        try:
            writer.flatten_annotations()
        except Exception:
            # Some versions may not have this; still save cleared values
            pass

        # Write output
        with open(output_path, "wb") as f:
            writer.write(f)
        
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False


def main():
    # Get the current directory
    current_dir = Path(".")
    output_dir = Path("cleared_pdfs")
    
    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)
    
    # Find all PDF files, excluding already processed ones and test files
    pdf_files = []
    for pdf_file in current_dir.glob("*.pdf"):
        # Skip files that are already cleared, flattened, or test files
        if "_cleared" not in pdf_file.name and "_flattened" not in pdf_file.name and "test" not in pdf_file.name.lower() and "blank" not in pdf_file.name.lower():
            pdf_files.append(pdf_file)
    
    print(f"Found {len(pdf_files)} PDF file(s) to process...\n")
    
    successful = 0
    failed = 0
    
    for pdf_file in pdf_files:
        # Create output path in the cleared_pdfs folder
        output_path = output_dir / pdf_file.name
        
        print(f"Processing: {pdf_file.name}...", end=" ")
        
        if clear_and_flatten_pdf(str(pdf_file), str(output_path)):
            print(f"[OK] -> {output_path}")
            successful += 1
        else:
            print(f"[FAILED]")
            failed += 1
    
    print(f"\nCompleted: {successful} successful, {failed} failed")
    print(f"Output folder: {output_dir.absolute()}")


if __name__ == "__main__":
    main()

